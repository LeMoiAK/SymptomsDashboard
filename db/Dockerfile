FROM postgres:16-alpine

ENV PGDATA=/var/lib/postgresql/data/pgdata

COPY postgres.conf /etc/postgresql/postgresql.conf
COPY pg_hba.conf /etc/postgresql/pg_hba.conf

RUN chown -R postgres:postgres /etc/postgresql

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]