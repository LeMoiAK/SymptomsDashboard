#!/bin/bash
set -e

if [ -z "$APP_DB_PASSWORD" ]; then
  echo "ERROR: APP_DB_PASSWORD is not set"
  exit 1
fi

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER app_user WITH PASSWORD '${APP_DB_PASSWORD}';

    GRANT CONNECT ON DATABASE app_db TO app_user;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname app_db <<-EOSQL
    GRANT USAGE ON SCHEMA public TO app_user;

    GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES IN SCHEMA public
    TO app_user;

    ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
EOSQL