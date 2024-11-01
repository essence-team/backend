# Mark DB Backend


# DEV BUILD
1. `conda create -n essence_backend python=3.11`
2. `conda activate essence_backend`
3. `pip install -r requirements/dev.txt`
4. `pre-commit install` — установка прекоммитов
5. `pre-commit run --all-files` — проверка кодстайла (будет запускаться автоматически при коммитах)

Также для тестирования можно поднять свой psql и elk: `source docker/deploy.sh up --env`

Для локального тестирования использовать также `source docker/deploy.sh up --app`

PSQL, elk при локальном тестировании останавливать каждый раз не нужно, поэтому используем остановку только сервера: `source docker/deploy.sh stop --app`
