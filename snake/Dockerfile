FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git
RUN pip install --upgrade pip

COPY requirements.txt /app/snake/requirements.txt
RUN pip install -r /app/snake/requirements.txt
COPY . /app/snake/

CMD sleep 5 && cd /app/snake && celery worker -Q analysis --loglevel info -E
