# dependencies

1. django
2. celery
3. gunicorn
4. pillow
5. pydantic
6. uvicorn
7. psycopg2-binary

dev dependencies:
1. ruff - code linting and formatter

# code linting and formating 

use `ruff check`, for see linting errors
`ruff check --select I001,E501 --fix`
`ruff check --ignore E501`

# testing 
`cd backend`
activate venv
`python manage.py test`

## tests coverages
```shell
cd src
coverage run manage.py test
coverage report
```

html report: `coverage html -d ../tests_coverage`


# documentation

[read here](./docs/README.md)

# files and dir

- src - has entire django's project sources, so it could be effectevely cached
  while building docker image.

  - src/main - is the django's project folder. But it's also has the main router in it
    and also global-wide template files.
  - src/blog, src/users - django's app dirs.
  - src/manage.py - is used by django for executing commands.\

- docs documentation folder
  - build 
  - source

- proproject.toml, uv.lock, .python-version - UV related files.
- Dockerfile, django-entrypoint.sh, .dockerignore - Docker related files.
- .gitignore - list of GIT's ignored files.
- .venv - Python's virtual environment.