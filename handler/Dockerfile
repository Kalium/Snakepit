FROM python:latest
RUN apt-get update && apt-get install -y git curl

RUN groupadd -r handler && useradd --no-log-init -r -g handler handler -d /app/handler
WORKDIR /app/handler
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app/handler
RUN chmod +x /app/handler/rules.sh
USER handler

CMD ./rules.sh && celery worker -Q scoring --loglevel info -E
