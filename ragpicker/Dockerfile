FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git python-dev libssl-dev
RUN pip install --upgrade pip

ADD . /app/ragpicker/
RUN pip install -r /app/ragpicker/requirements.txt

CMD cd /app/ragpicker && python /app/ragpicker/ragpicker.py -i
