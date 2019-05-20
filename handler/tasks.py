"""
Tasks is responsible for describing the labors performed by handler.

This file contains the logic for evaluting rules and scoring analysis data.
"""

import re
import os
import requests
import json
from celery import Celery

app = Celery('tasks', )
app.config_from_object('celeryconfig')
pit_url = os.getenv('PIT_URL', 'http://pit:5000/').rstrip('/')
post_headers = {'Accept': 'application/json',
                'Content-Type': 'application/json'}

# This is needed to write back scored results.
ANALYSIS_TEMPLATE = {
    'id': None,
    'score': None
}


def getAnalysis(analysis_id):
    """Grabs data from pit."""
    resp = requests.get('/'.join([pit_url, 'analysis', str(analysis_id)]))

    analysis = json.loads(resp.content)
    return analysis


def getRules(analysis_key):
    """Grabs rules for evaluation against data from pit."""
    resp = requests.get('/'.join([pit_url, 'rule', analysis_key]))

    if resp.status_code == 200:
        rules = json.loads(resp.content)
        if not isinstance(rules, list):
            rules = [rules]
    else:
        rules = []
    return rules


def evaluateRules(analysis, rules):
    """Perform evaluation and calculate score totals."""
    score = 0
    for rule in rules:
        if re.match(rule['matcher'], str(analysis['data'])):
            score = score + int(rule['value'])
    return score


def saveScore(analysis_id, score):
    """Save calculated score back to pit."""
    a = ANALYSIS_TEMPLATE.copy()
    a['id'] = analysis_id
    a['score'] = score

    resp = requests.patch('/'.join([pit_url, 'analysis', str(analysis_id)]),
                          data=json.dumps(a), headers=post_headers)
    resp.raise_for_status()


# For an analysis item:
# * Fetch the item.
# * Fetch all relevant rules.
# * Evaluate each rule, keeping a running total of score.
# * Save score to analysis item.
@app.task(name="snakepit.scoring.score", throws=(requests.HTTPError))
def score(analysis_id):
    """Glue together all the helpers to fully score analysis."""
    analysis = getAnalysis(analysis_id)
    rules = getRules(analysis['key'])
    score = evaluateRules(analysis, rules)

    if score != 0:
        saveScore(analysis_id, score)
    return None
