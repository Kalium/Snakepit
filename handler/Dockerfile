FROM python:latest
RUN apt-get update && apt-get install -y git curl

COPY requirements.txt /app/handler/requirements.txt
RUN pip install -r /app/handler/requirements.txt
COPY . /app/handler/
RUN chmod +x /app/handler/rules.sh

CMD /app/handler/rules.sh && cd /app/handler && celery worker -Q scoring --loglevel info -E
