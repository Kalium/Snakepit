import os
import requests
import json
from celery import Celery

app = Celery('tasks', )
app.config_from_object('celeryconfig')
app.conf.task_routes = {'snakepit.analysis.*': {'queue': 'analysis'},
                        'snakepit.scoring.*': {'queue': 'scoring'}}
pit_url = os.getenv('PIT_URL', 'http://pit:5000/')
viper_url = os.getenv('VIPER_URL', 'http://viper:8080/')
post_headers = {'Accept': 'application/json',
                'Content-Type': 'application/json'}

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


@app.task(name="snakepit.scoring.score")
def triggerScoring(analysis_id):
    pass


@app.task(name="snakepit.analysis.start")
def fanout(sha256):
    # throwInPit can be done by a worker
    # but we want it as a general precursor to ensure
    # that the object is there before we start creating children
    throwInPit(sha256)
    getDataByHash.delay(sha256)


@app.task(throws=(requests.HTTPError))
def throwInPit(sha256):
    i = ITEM_TEMPLATE.copy()
    i['hash'] = sha256

    resp = requests.post(pit_url + 'item', data=json.dumps(i),
                         headers=post_headers)
    resp.raise_for_status()


@app.task(name="snakepit.analysis.getDataByHash", throws=(requests.HTTPError))
def getDataByHash(sha256):
    # Grabs the data from the initial static analysis done by ragpicker
    # and Viper, then adds it to snakes data section
    payload = {'sha256': sha256}
    resp = requests.post(viper_url + "file/find", payload,
                         headers=post_headers)
    resp.raise_for_status()
    result = resp.json()
    data = {}
    data = result['results']['default']
    saveAnalysis(sha256=sha256, key="getDataByHash", data=data)
