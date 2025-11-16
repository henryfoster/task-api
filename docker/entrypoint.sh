#!/bin/bash

set -e # makes the script exit if one command fails

while ! uv run docker/health_check.py; do
  echo "Database not ready waiting..."
  sleep 1
done
echo "Database is ready!"

echo "Running migrations ..."
uv run alembic upgrade head

exec "$@" # runs whatever is passed to the command
