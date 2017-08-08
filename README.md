# Snakepit

## About
Snakepit is a docker-enabled framework for analysis and triage of binaries in a networked environment. It's designed for the easy addition of whatever tools you want to use. Analysis functionality is added in snake. Scoring and rules are handled in handler. As a result, plugins are split between snake and handler.

## Why
We all need hobbies.

## Notes
* Added a small API CLI tool for Viper which should come in use since we aren't running the web interface.
* No oletools in viper. Not a big loss here.
* At this point you'll have to run the ragpicker container manually. I suggest mounting a volume and feeding it directories. If you look at ragpicker/Dockerfile, you'll see an example of this.
* Resetting a score for re-analysis is left as an exercise. handler's `saveScore` shows how to do it.

## Using
* `docker-compose build`
* `docker-compose up`
* Direct your browser to http://localhost:5555/tasks to see what work has been done.
* Use Swagger at http://localhost:5557/ to poke at pit's API.

## Components

### Storage
* redis - This is where the Celery job queue lives.
* viper-db - A postgres database that backs the Viper binary storage system.
* pit-db - A postgres database that backs the pit data storage API.

### Infrastructure
* viper - A storage and management system for binaries.
* ragpicker - A binary ingestion system.
* flower - A management and monitoring UI for Celery.
* swagger - A system for viewing API documentation in a web browser. Pit's mostly works.

### Core Services
* pit - An API for storing and retrieving analysis results and binary parent/child relationships. Minimal logic, could be put behind a load-balancer with several instances.  Items are identified by SHA256. Items may have a parent. Analysis data are identified by SHA256 of the item and the key (read: name of analysis job) of the datum.
* snake - A bare-bones framework for doing asynchronous analysis tasks. Stores its results in pit. Designed to be run in clusters.
* handler - A scorer, driven by rules served by pit.

## Accessing Things
* Flower binds to port 5555.
* Viper API is on port 5556.
* Swagger is on port 5557. By default it shows pit's docs.
* Pit is on port 5558.

## Licensing
Ragpicker, Viper, Flower, Celery and assorted Python packages are all under their own licenses.
Pit, snake, handler, and the organizational work in this repo, are MIT licensed.

## TODO
* A scorer that doesn't suck and isn't based on regexen. I hate regexen. They're also all I can think of that isn't eval().
