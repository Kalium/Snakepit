FROM ubuntu:latest
RUN apt-get update && apt-get install -y python-pip git python-dev libssl-dev
RUN pip install --upgrade pip

COPY . /app/ragpicker/
RUN pip install -r /app/ragpicker/requirements.txt

CMD cd /app/ragpicker && sleep 7 && python /app/ragpicker/ragpicker.py -p 1 -d /app/ragpicker/tools/
