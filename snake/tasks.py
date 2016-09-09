import os
import requests
import json
from celery import Celery

app = Celery('tasks', )
app.config_from_object('celeryconfig')
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


@app.task(name="snakepit.start")
def fanout(sha256):
    # throwInPit can be done by a worker
    # but we want it as a general precursor to ensure
    # that the object is there before we start creating children
    throwInPit(sha256)
    fileLength.delay(sha256)


@app.task(throws=(requests.HTTPError))
def throwInPit(sha256):
    i = ITEM_TEMPLATE.copy()
    i['hash'] = sha256

    resp = requests.post(pit_url + 'item', data=json.dumps(i),
                         headers=post_headers)
    resp.raise_for_status()


@app.task(throws=(requests.HTTPError))
def fileLength(sha256):
    resp = requests.get(viper_url + "file/get/" + sha256)
    resp.raise_for_status()
    size = len(resp.content)
    saveAnalysis(sha256=sha256, key="fileLength",
                 data=json.dumps({"length": size}))
