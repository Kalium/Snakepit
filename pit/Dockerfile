FROM ubuntu:latest
# RUN apt-get update && apt-get install -y libfuzzy-dev python-pip git libssl-dev libffi-dev swig libpq-dev python-dev
RUN pip install --upgrade pip

ADD . /app/pit/
RUN pip install -r /app/pit/requirements.txt

RUN python app.py db upgrade && python app.py
