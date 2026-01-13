# services

1. db
2. rabbitmq
3. django
4. celery

# launch

using dev environment: 
`docker compose -f docker-compose.dev.yml up`

# deployment
1. set desired parameters in .env file and backend/src/main
2. `docker compose -f docker-compose.yml up`

## scaling challenges

[!WARNING]
it's impossible to move workers to another server, because task process_avatar
stores image on django's storage. Use NFS for temp files or 
save entire image to the db 