#!/usr/bin/env bash
set -euo pipefail

host="${POSTGRES_HOST:-db}"
port="${POSTGRES_PORT:-5432}"

>&2 echo "Waiting for PostgreSQL at $host:$port..."
for i in {1..30}; do
  if nc -z "$host" "$port"; then
    >&2 echo "PostgreSQL is up"
    break
  fi
  sleep 1
  if [ "$i" -eq 30 ]; then
    >&2 echo "PostgreSQL did not become available in time"; exit 1
  fi
done

# Run migrations
python manage.py migrate --noinput
# Optionally seed if flag provided
if [ "${SEED_FAKESTORE:-0}" = "1" ]; then
  python manage.py import_all
fi

# Start server
exec python manage.py runserver 0.0.0.0:8000
