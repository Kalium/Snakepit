FROM ubuntu:latest
RUN apt-get update && apt-get install -y libfuzzy-dev python-pip git libssl-dev libffi-dev swig libpq-dev python-dev
RUN pip install --upgrade pip

COPY . /app/viper/
RUN pip install -r /app/viper/requirements.txt
RUN cd /app/viper && make install
COPY viper.conf /etc/viper/viper.conf

EXPOSE 8080
CMD sleep 5 && python /app/viper/viper-api -H 0.0.0.0
