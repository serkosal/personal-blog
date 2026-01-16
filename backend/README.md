# dependencies | Зависимости 

1.  `django` - Web-framework | Веб-фреймворк.
2.  `django-taggit` - Adds tags for Django's models.
3.  `django-vite` - Integrations for frontend's build system.
4.  `celery` - Task queue.
5.  `uvicorn` - Web-server for django. 
6.  `gunicorn` - Async http workers for uvicorn.
7.  `pillow` - For image manipulation, required by Django's Image Field.
8.  `pydantic` - For data validation.
9.  `psycopg2-binary` - Required for PostgreSQL.

## dev dependencies | Зависимости для разработки
1.  `coverage` - 
    tool for analyse code's test coverage | 
    утилита для анализа покрытия кода тестами
2.  `ruff` - 
    tool for linting and auto-formatting Python's code | 
    утилита для линтовки и авто-форматирования кода Питона
3.  `sphinx` - 
    tool for documentation generation | 
    утилита для генерации документации
4.  `sphinx-rtd-theme` -
    `Read the docs` theme for doc generator `Spinx` | 
    тема `Read the docs` для генератора документации `Spinx` 

# code linting and formating | линтовка и авто-форматирование кода.

use `ruff check`, for see linting errors
`ruff check --select I001,E501 --fix`
`ruff check --ignore E501`

# testing | Тестирование кода.
`cd backend`
activate venv
`python manage.py test`

## tests coverages | Покрытие тестами.
```shell
cd src
coverage run manage.py test
coverage report
```

html report: `coverage html -d ../tests_coverage`


# documentation | Документация кода

[read here](./docs/README.md)

# files and dir | Файлы и директории

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