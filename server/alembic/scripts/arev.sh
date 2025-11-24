#!/bin/bash

# Usage: alembic/scripts/arev.sh "description of change"

if [ -z "$1" ]; then
  echo "Error: Missing description"
  echo "Usage: alembic/scripts/arev.sh \"description of change\""
  exit 1
fi

DESC=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
REV_ID=$(date +"%Y%m%d_%H%M")

alembic revision --autogenerate -m "$DESC" --rev-id "$REV_ID"