#!/bin/bash


BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${BASE_DIR}/src

env_celery=$(pipenv --venv)/bin/celery
mycmd=($env_celery worker -A celery_worker.celery --loglevel=info)

"${mycmd[@]}"

