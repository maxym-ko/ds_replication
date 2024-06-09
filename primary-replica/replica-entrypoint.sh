#!/bin/bash
set -e

# Check if the data directory is empty
if [ -z "$(ls -A /var/lib/postgresql/data)" ]; then
  echo "Data directory is empty. Starting base backup..."
  until pg_basebackup --pgdata=/var/lib/postgresql/data -R --slot=replication_slot --host=postgres_primary --port=5432
  do
    echo "Waiting for primary to connect..."
    sleep 1s
  done
  echo "Backup done, starting replica..."
  chmod 0700 /var/lib/postgresql/data
else
  echo "Data directory is not empty. Skipping base backup..."
fi

exec "$@"
