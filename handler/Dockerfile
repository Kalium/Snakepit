FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git
RUN pip install --upgrade pip

COPY . /app/handler/
RUN pip install -r /app/handler/requirements.txt

CMD sleep 5 && cd /app/handler && celery worker -Q scoring --loglevel info -E
