FROM      python

# WARNING: BE SURE NOT TO USE THE WORD 'FLOWER' IN THE ENV VARS
# E.G. VIA LINKING OR MAESTRO-NG: THEY HAVE A SPECIAL MEANING IN FLOWER.

RUN       pip install redis
RUN       pip install flower

# Default port
EXPOSE    5555

CMD       flower --port=5555 --broker=redis://$REDIS_HOST:$REDIS_PORT/$REDIS_DATABASE
