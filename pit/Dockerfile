FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git python-dev libpq-dev
RUN pip install --upgrade pip

COPY requirements.txt /app/pit/requirements.txt
RUN pip install -r /app/pit/requirements.txt
COPY . /app/pit/

CMD sleep 5 && cd /app/pit && FLASK_APP=app.py flask run -h 0.0.0.0
