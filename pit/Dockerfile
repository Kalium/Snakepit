FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git python-dev libpq-dev
RUN pip install --upgrade pip

ADD . /app/pit/
RUN pip install -r /app/pit/requirements.txt

CMD sleep 5 && cd /app/pit && FLASK_APP=app.py flask run -h 0.0.0.0
