# services | Сервисы

1. frontend
2. django
3. nginx
4. db 
5. rabbitmq
6. celery

# WARNING | ВНИМАНИЕ !
[!WARNING]
**All commands provided in README.md files must be executed from their directories!**
**Все команды из README.md файлы должны выполняться из тех же директорий!** 

# Launch | Запуск

using configuration for development | используя конфигурацию для разработки
```shell
docker compose -f docker-compose.dev.yml up
```

using configuration for production | используя конфигурацию для продакшена
```shell
docker compose up
```

## Standalone launch (without Docker) | Запуск бэкенда автономно (без Docker'а)

1.  build frontend static files | собрать файлы фронта:
    ```shell
        cd frontend
        npm install
        npm run build
    ```

2.  download backend's dependencies | скачать зав-ти бэкенда:
    ```shell
        cd ../backend
    ```

    -   Using `pip` | Используя `pip`:
        ```shell
            ######################## FOR Windows | Для Windows #####################
            python -m venv .venv                                                   #
            .venv/bin/activate.bat                                                 #
            ########################################################################

            ############## FOR Linux, MacOs, WSL | Для Linux, MacOS, WSL  ##########
            python3 -m venv .venv                                                  #
            source .venv/bin/activate                                              #
            ########################################################################
        ```

    -   Or using `uv` | Или используя `uv`
        ```shell
            uv sync
        ```

3.  Run development server | Запустить сервер для разработки python:
    -   Using `uv` | Используя `uv`:
        ```shell 
            uv run python 
        ```
    -   Without `uv` | Без `uv`:
        ```shell 
            python manage.py runserver
        ```


# environment and configuration | Среда и конфигурация
environment files stored in `secrets` folder | Файлы с переменными среды 
расположены в папке `secrets`.

# deployment | Деплой
1.  set desired parameters in .env file and backend/src/main/settings.py
2.  `docker compose up`

## scaling challenges | Сложности масштабирования

[!WARNING]
it's impossible to move workers to another server, because service `celery` 
needs files from the same host machine as `django`. 
Use `NFS` to share files across machines.