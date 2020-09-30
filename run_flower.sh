#!/bin/bash


BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${BASE_DIR}/src

env_celery=$(pipenv --venv)/bin/flower
mycmd=($env_celery -A celery_worker.celery --port=5555)

"${mycmd[@]}"

