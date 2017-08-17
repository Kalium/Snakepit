"""Responsible for configuring and routing this Celery worker."""
import os

CELERY_IMPORTS = ('tasks', )
BROKER_URL = os.getenv('BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TRACK_STARTED = True
CELERY_QUEUES = {
    "analysis": {
        "binding_key": "snakepit.analysis.#",
    },
    "scoring": {
        "binding_key": "snakepit.scoring.#",
    },
}
