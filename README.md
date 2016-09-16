# Snakepit

Snakepit is a docker-enabled framework for analysis and triage of binaries in a networked environment. It's designed for the easy addition of whatever tools you want to use. There's an example called "fileLength" demonstrating analysis.

Notes:
* No oletools in viper. Not a big loss here.
* At this point you'll have to run the ragpicker container manually. I suggest mounting a volume and feeding it directories. If you look at ragpicker/Dockerfile, you'll see an example of this.

Using:
* `docker-compose build`
* `docker-compose up`
* Direct your browser to http://localhost:5555/tasks to see what work has been done.
* Use Swagger at http://localhost:5557/ to poke at pit's API.

Components:
* redis - This is the job queue.
* viper-db - A postgres database that backs the Viper binary storage system.
* pit-db - A postgres database that backs the pit data storage API.
* flower - A management UI for Celery.
* viper - A storage and management system for binaries.
* ragpicker - A binary ingestion system.
* pit - An API for storing and retrieving analysis results and binary parent/child relationships. Minimal logic, could be put behind a load-balancer with several instances.  Items are identified by SHA256. Items may have a parent. Analysis data are identified by SHA256 of the item and the key (read: name of analysis job) of the datum.
* swagger - A system for viewing API documentation. Pit's mostly works.
* snake - A bare-bones framework for doing asynchronous analysis tasks. Stores its results in pit. Designed to be run in clusters.

Access Things:
* Flower binds to port 5555.
* Viper API is on port 5556.
* Swagger is on port 5557. By default it shows pit's docs.
* Pit is on port 5558.

Licensing:
Ragpicker, Viper, Flower, Celery and assorted Python packages are all under their own licenses.
Pit, Snake, and the organizational work in this repo, are MIT licensed.

TODO:
* Scorer. This requires a rules engine and a service to offer them up.
