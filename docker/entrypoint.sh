#!/usr/bin/env bash
set -euo pipefail

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL is not set"
  exit 1
fi

until pg_isready --dbname="$DATABASE_URL" > /dev/null 2>&1; do
  echo "Waiting for PostgreSQL to become available"
  sleep 1
done

echo "PostgreSQL is available"
exec "$@"
