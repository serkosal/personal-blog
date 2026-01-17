# services <br> Сервисы

1. frontend
2. django
3. nginx
4. db 
5. rabbitmq
6. celery

# WARNING<br>ВНИМАНИЕ !
[!WARNING]<br>
**All commands provided in README.md files must be executed from their directories!** <br>
**Все команды из README.md файлы должны выполняться из тех же директорий!** 

# Launch<br>Запуск

using configuration for development<br>
используя конфигурацию для разработки
```shell
docker compose -f docker-compose.dev.yml up
```

using configuration for production<br> 
используя конфигурацию для продакшена
```shell
docker compose up
```

## Standalone launch (without Docker)<br>Запуск бэкенда автономно (без Docker'а)

1.  build frontend static files<br>
    собрать файлы фронта:
    ```shell
        cd frontend
        npm install
        npm run build
    ```
nd's depend
2.  download backend dependencies<br>
    скачать зав-ти бэкенда:
    ```shell
        cd ../backend
    ```

    -   Using `pip`<br>
        Используя `pip`:
        ```shell
            ######################## FOR Windows | Для Windows #################
            python -m venv .venv                                               #
            .venv/bin/activate.bat                                             #
            ####################################################################

            ############## FOR Linux, MacOs, WSL | Для Linux, MacOS, WSL  ######
            python3 -m venv .venv                                              #
            source .venv/bin/activate                                          #
            # If using fish shell: source .venv/bin/activate.fish              #
            ####################################################################
        ```

    -   Or using `uv`<br>
        Или используя `uv`
        ```shell
            uv sync
        ```

3. Set environment variables `DEBUG=1` and `USE_SQLITE=1`

4.  Configure and run development server<br>
    Настроить и запустить сервер для разработки python:

    -   Using `uv` <br> Используя `uv`:
        ```shell
            uv run python manage.py migrate
            uv run python manage.py collectstatic
            uv run python manage.py runserver
        ```
    -   Without `uv` <br> Без `uv`:
        **Make sure that python venv is activated**
        ```shell 
            python manage.py runserver
            python manage.py migrate
            python manage.py collectstatic
        ```


# environment and configuration<br>Среда и конфигурация
environment files stored in `secrets` folder<br> 
Файлы с переменными среды расположены в папке `secrets`.

# deployment <br> Деплой
1.  set desired parameters in .env file and backend/src/main/settings.py
2.  `docker compose up`

## scaling challenges<br>Сложности масштабирования

[!WARNING]<br>
it's impossible to move workers to another server, because service `celery` 
needs files from the same host machine as `django`. 
Use `NFS` to share files across machines.