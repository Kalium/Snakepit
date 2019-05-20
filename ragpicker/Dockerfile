FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git python-dev libssl1.0-dev
RUN pip install --upgrade pip

COPY requirements.txt /app/ragpicker/requirements.txt
RUN pip install -r /app/ragpicker/requirements.txt
COPY . /app/ragpicker/

CMD cd /app/ragpicker && python /app/ragpicker/ragpicker.py -p 1 -d /app/ragpicker/tools/
