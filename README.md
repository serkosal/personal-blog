# other languages
1. На русском [здесь](./README_RU.md)


# Features
1.  Backend and frontend integration (Django + Tailwind) supporting: 
    - either standalone or containerized environments.
    - either development (supports HMR) or production stages.  

2.  Deserialization and validation of the text rich data, and its rendering. 
    
3.  Asynchronous tasks runned by `Celery`. For this time point there is only 
    tasks for avatar's processing - creation of differently sized thumbnails.
    In the future there will be tasks for email, push and messengers 
    notifications.

4.  SEO optimisation using server side rendering. In the future this process 
    will be analyzed further for optimisations using caching.

5.  Keeping a reasonable size of the pages. I'm not a big fan of pointlessly 
    moving electrons or photons around the globe.  

# WARNING
[! WARNING ]<br>
**All provided commands must be executed relative to corresponding README.md files !** 

# Developer Launch

You could run run this project either using `docker-compose` (one liner) or as 
standalone services:
-   Use the [standalone](#as-standalone-without-docker-docker-compose) 
    variant if you experienced enough to manage project 
    dependencies for both JS and python django's projects, set environment 
    variables and possibly to independently sort thing out.
-   Or use [docker](#using-docker-compose-one-liner) variant otherwise.

## using docker compose (one-liner).
```shell
docker compose -f docker-compose.dev.yml up
```
By default:
-   `SQLite` is used as database 
-   Django's `debug mode` is turned on 
-   Frontend server is running and working in `hot module reload` mode 
    (frontend sources could be modified and changes is visible in real time).

These behaivour is specified in `environment variables` which docker gets from 
[this](./secrets/.dev.env) file.

## as standalone (without docker, docker compose).

1.  Use [this](./frontend/README.md) instruction to either build or run frontend
    server (*Recomended*) to provide backend with required styles, scripts, etc.

2.  Set environment variables: 
    -   You could just use predefined variables recommended to development from 
        [there](./secrets/.dev.env).
    -   or set everyting manually, as described [here](./secrets/README.md). 

3.  Optionally run other services, which are described [there](#services).  <br>
    Without other services some site's functionality won't work.

# services

1. frontend - could be run as server which supports `HMR`. 
2. django
3. nginx
4. db 
5. rabbitmq
6. celery

# environment and configuration
environment files stored in `secrets` folder<br> 
Файлы с переменными среды расположены в папке `secrets`.

# deployment
1.  set desired parameters in .env file and backend/src/main/settings.py
2.  `docker compose up`

This section isn't done yet! 

## scaling challenges

[!WARNING]<br>
it's impossible to move workers to another server, because service `celery` 
needs files from the same host machine as `django`. 
Use `NFS` to share files across machines.