"""
Tasks is responsible for describing the many labors performed by snake.

This file contains the logic for saving blobs, triggering analysis,
saving analysis data, and handling asynchronous jobs.
"""

import os
import requests
import json
import CuckooAPI
import time
from celery import Celery
from celery.utils.log import get_task_logger
from urllib.parse import urlparse

app = Celery('tasks', )
app.config_from_object('celeryconfig')
app.conf.task_routes = {'snakepit.analysis.*': {'queue': 'analysis'},
                        'snakepit.scoring.*': {'queue': 'scoring'}}

logger = get_task_logger(__name__)
pit_url = os.getenv('PIT_URL', 'http://pit:5000/')
viper_url = os.getenv('VIPER_URL', 'http://viper:8080/')
cuckoo_url = os.getenv('CUCKOO_HOST', '')
post_headers = {'Accept': 'application/json',
                'Content-Type': 'application/json'}
cuckoo_user = os.getenv('CUCKOO_USER', None)
cuckoo_pass = os.getenv('CUCKOO_PASSWD', None)

ITEM_TEMPLATE = {
    'hash': None,
    'parent': None
}

ANALYSIS_TEMPLATE = {
    'item_hash': None,
    'key': None,
    'data': None
}


def saveAnalysis(sha256, key, data):
    """Responsible for writing JSON blobs to pit."""
    a = ANALYSIS_TEMPLATE.copy()
    a['item_hash'] = sha256
    a['key'] = key
    a['data'] = data

    resp = requests.post(pit_url + 'analysis', data=json.dumps(a),
                         headers=post_headers)
    resp.raise_for_status()

    # Analysis saved. Now trigger scoring job.
    ret = json.loads(resp.content)
    triggerScoring.delay(ret['id'])


def getItem(sha256):
    """Grab binary from viper."""
    pass


@app.task(name="snakepit.scoring.score")
def triggerScoring(analysis_id):
    """Celery's placeholder."""
    pass


@app.task(name="snakepit.analysis.start")
def fanout(sha256):
    """Centralized save-and-do-work function."""
    # throwInPit can be done by a worker
    # but we want it as a general precursor to ensure
    # that the object is there before we start creating children
    throwInPit(sha256)
    getDataByHash.delay(sha256)
    submitToCuckoo.delay(sha256)


@app.task(throws=(requests.HTTPError))
def throwInPit(sha256):
    """Save the blob."""
    i = ITEM_TEMPLATE.copy()
    i['hash'] = sha256

    resp = requests.post(pit_url + 'item', data=json.dumps(i),
                         headers=post_headers)
    if resp.status_code != requests.codes.bad_request:
        # "Bad Request" means a unique item violation, which means it's already
        # there. Move on!
        resp.raise_for_status()
    elif resp.status_code == requests.codes.bad_request:
        logger.info('Item ' + sha256 + ' is a duplicate of a known item')


@app.task(name="snakepit.analysis.viperData", throws=(requests.HTTPError))
def getDataByHash(sha256):
    """Grab all data Viper has. Save."""
    payload = {'sha256': sha256}
    resp = requests.post(viper_url + "file/find", payload,
                         headers=post_headers)
    resp.raise_for_status()
    result = resp.json()
    data = {}
    data = result['results']['default']
    saveAnalysis(sha256=sha256, key="viperData", data=data)


def getCuckooApiInstance():
    """Return a functional CuckooAPI instance."""
    # Bail if cuckoo not configured.
    if not cuckoo_url:
        return
    parsed = urlparse(cuckoo_url)
    if cuckoo_pass is not None:
        return CuckooAPI.CuckooAPI(host=parsed.hostname, proto="https",
                                   user=cuckoo_user, passwd=cuckoo_pass)
    else:
        return CuckooAPI.CuckooAPI(host=parsed.hostname, proto="https")


@app.task(name="snakepit.analysis.cuckoo.start", throws=(requests.HTTPError))
def submitToCuckoo(sha256):
    """Submit to Cuckoo. Kick off poller for results."""
    url = ''.join([viper_url + "file/get/" + sha256])
    request = requests.get(url, stream=True)

    with open(sha256, 'wb') as f:
        # Read and write in chunks
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    api = getCuckooApiInstance()
    resp = api.submitfile(sha256)
<<<<<<< HEAD
    # return resp['task_id']
=======
>>>>>>> 666e7ff667f6d0b2ec9b30d7b326d1ecd3e79c5b
    pollCuckoo.delay(sha256, resp['data']['task_ids'])


@app.task(name="snakepit.analysis.cuckoo.poll", throws=(requests.HTTPError))
def pollCuckoo(sha256, task_id):
    """Poll Cuckoo for completed analysis."""
    api = getCuckooApiInstance()
    status = api.taskstatus(task_id)
    if status['data'] == 'reported':
        # It's finished! Time to grab the report.
        finishCuckoo.delay(sha256, task_id)
    else:
        time.sleep(5)
        pollCuckoo.delay(sha256, task_id)


@app.task(name="snakepit.analysis.cuckoo.finish", throws=(requests.HTTPError))
def finishCuckoo(sha256, task_id):
    """Grab finished Cuckoo report. Save."""
    api = getCuckooApiInstance()
    report = api.taskreport(task_id)
    saveAnalysis(sha256, "cuckoo", report)
    pass
