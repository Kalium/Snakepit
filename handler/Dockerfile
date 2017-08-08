FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git curl
RUN pip install --upgrade pip

COPY requirements.txt /app/handler/requirements.txt
RUN pip install -r /app/handler/requirements.txt
COPY . /app/handler/
RUN chmod +x /app/handler/rules.sh

CMD sleep 5 && /app/handler/rules.sh && cd /app/handler && celery worker -Q scoring --loglevel info -E
