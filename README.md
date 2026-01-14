# services

1. db
2. rabbitmq
3. django
4. celery

# launch

using dev environment: 
`docker compose -f docker-compose.dev.yml up`

# environment and configuration
DJANGO_DEBUG_ENABLED=0
DJANGO_SECRET_KEY='django-secret-key'

POSTGRES_DB="site"
POSTGRES_USER="postgres-user"
POSTGRES_PASSWORD='password'
POSTGRES_HOST="db"
POSTGRES_PORT='5432'

RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest


# deployment
1. set desired parameters in .env file and backend/src/main
2. `docker compose -f docker-compose.yml up`

## scaling challenges

[!WARNING]
it's impossible to move workers to another server, because task process_avatar
stores image on django's storage. Use NFS for temp files or 
save entire image to the db 