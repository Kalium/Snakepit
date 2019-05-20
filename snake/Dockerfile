FROM python:latest
RUN apt-get update && apt-get install -y git curl

RUN groupadd -r snake && useradd --no-log-init -r -g snake snake -d /app/snake
WORKDIR /app/snake
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app/snake
USER snake

CMD celery worker -Q analysis --loglevel info -E
