# Snakepit

Notes:
* No oletools in viper. Not a big loss here.

Using:
* `docker-compose build`
* `docker-compose up`

Components:
* redis - This is the job queue.
* viper-db - A postgres database that backs the Viper binary storage system.
* pit-db - A postgres database that backs the pit data storage API.
* flower - A management UI for Celery.
* viper - A storage and management system for binaries.
* ragpicker - A binary ingestion system.
* pit - An API for storing and retrieving analysis results and binary parent/child relationships.
* swagger - A system for viewing API documentation. In this case pit's.

Access Things:
* Flower binds to port 5555.
* Viper API is on port 5556.
* Swagger is on port 5557. By default it shows pit's docs.
* Pit is on port 5558.

At this point you'll have to run the ragpicker container yourself.
I suggest mounting a volume and feeding it files.

Licensing:
Ragpicker, Viper, Flower, Celery and assorted Python packages are all under their own licenses.
Pit, and the organizational work in this repo, are MIT licensed.

TODO:
Create celery job runner.
Give celery job runner some example jobs.
