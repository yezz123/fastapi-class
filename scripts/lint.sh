#!/usr/bin/env bash

set -e
set -x

mypy --show-error-codes fastapi_class tests
