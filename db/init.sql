CREATE USER app_user WITH PASSWORD 'replace_me';

ALTER ROLE app_user SET client_encoding TO 'utf8';
ALTER ROLE app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE app_user SET timezone TO 'UTC';

GRANT CONNECT ON DATABASE app_db TO app_user;

\c app_db

GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;