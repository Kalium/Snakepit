FROM python:latest
RUN apt-get update && apt-get install -y git curl

COPY requirements.txt /app/snake/requirements.txt
RUN pip install -r /app/snake/requirements.txt
COPY . /app/snake/

CMD cd /app/snake && celery worker -Q analysis --loglevel info -E
