FROM python:latest
RUN apt-get update && apt-get install -y git python-dev libpq-dev libyaml-dev libyaml-0-2

COPY requirements.txt /app/pit/requirements.txt
RUN pip install -r /app/pit/requirements.txt
COPY . /app/pit/

CMD cd /app/pit && FLASK_APP=app.py flask run -h 0.0.0.0
