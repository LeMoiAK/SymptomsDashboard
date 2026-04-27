"""
Script to experiment with connecting to the PostgreSQL database and run requests.
"""

# Get env vars using pydantic
from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class DbConfig(BaseSettings):
    APP_DB_USER: str = Field(min_length=1)
    APP_DB_PASSWORD: str = Field(min_length=1)

config = DbConfig()

# Then connect to DB
print(f"User: {config.APP_DB_USER} | pass: {config.APP_DB_PASSWORD}")
import psycopg2
conn = psycopg2.connect(database = "app_db", 
                        user = config.APP_DB_USER, 
                        host = 'localhost',
                        password = config.APP_DB_PASSWORD,
                        port = 5432)

cur = conn.cursor()
cur.execute('SELECT * FROM patients;')
rows = cur.fetchall()
conn.commit()
conn.close()
for row in rows:
    print(row)