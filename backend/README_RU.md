# Зависимости 

1.  `django` - Web-framework | Веб-фреймворк.
2.  `django-taggit` - Adds tags for Django's models.
3.  `django-vite` - Integrations for frontend's build system.
4.  `celery` - Task queue.
5.  `uvicorn` - Web-server for django. 
6.  `gunicorn` - Async http workers for uvicorn.
7.  `pillow` - For image manipulation, required by Django's Image Field.
8.  `pydantic` - For data validation.
9.  `psycopg2-binary` - Required for PostgreSQL.

## Зависимости для разработки
1.  `coverage` -
    tool for analyse code's test coverage<br> 
    утилита для анализа покрытия кода тестами
2.  `ruff` -
    tool for linting and auto-formatting Python's code<br> 
    утилита для линтовки и авто-форматирования кода Питона
3.  `sphinx` -
    tool for documentation generation<br> 
    утилита для генерации документации
4.  `sphinx-rtd-theme` -
    `Read the docs` theme for doc generator `Spinx`<br> 
    тема `Read the docs` для генератора документации `Spinx` 

# линтовка и авто-форматирование кода.

use `ruff check`, for see linting errors
`ruff check --select I001,E501 --fix`
`ruff check --ignore E501`

# Тестирование кода.
`cd backend`
activate venv
`python manage.py test`

## Покрытие тестами.
```shell
cd src
coverage run manage.py test
coverage report
```

html report: `coverage html -d ../tests_coverage`


# Документация кода

[read here](./docs/README.md) | [читай здесь](./docs/README.md)

# Файлы и директории

-   `src` -
    this directory has entire django's project sources, so it could be 
    effectevely cached while docker builds image.

    -   `src/main` -
        is the django's project folder. But it's also has the main router in it
        and also global-wide template files.
    -   `src/blog`, `src/users` -
        django application's directories.
    -   `src/manage.py` -
        is used by django for executing commands.

-   `proproject.toml`, `uv.lock`, `.python-version`, `requirements.txt` -
    backend's project related files.
-   `Dockerfile`, `entrypoint.sh`, `entrypoint.dev.sh`, `.dockerignore` -
    Docker files which builds `django` and `celery` services.

-   `docs` - folder with backend's documentation:
    -   `build` 
    -   `source`

-   `test_coverage` -
    files with report of the test's coverage in `html` format. 

-   `.git` -
    version control system 
    -   `.gitignore` -
        list of files which are excluded from being monitored by version control 
        system `git`.
    -   `.gitkeep`

-   `.venv` -
    Python virtual environment directory.