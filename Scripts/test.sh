#!/usr/bin/env bash

set -e
set -x

echo "ENV=${ENV}"

export PYTHONPATH=.
pytest --cov=fastapi_class --cov=tests --cov-report=term-missing --cov-fail-under=80
