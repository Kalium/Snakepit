FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git
RUN pip install --upgrade pip

ADD . /app/snake/
RUN pip install -r /app/snake/requirements.txt

CMD sleep 5 && cd /app/snake && celery worker --loglevel info -E
