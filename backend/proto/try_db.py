"""
Script to experiment with connecting to the PostgreSQL database and run requests.
"""

# Get env vars using pydantic
from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class DbConfig(BaseSettings):
    APP_DB_USER: str = Field(min_length=1)
    APP_DB_PASSWORD: str = Field(min_length=1)
    DATABASE_URL: str = Field(min_length=1)

config = DbConfig()

# Then connect to DB
print(f"User: {config.APP_DB_USER} | pass: {config.APP_DB_PASSWORD}")

import sqlalchemy as db
engine = db.create_engine(f"postgresql://{config.APP_DB_USER}:{config.APP_DB_PASSWORD}@localhost:5432/app_db")
conn = engine.connect() 
output = conn.execute("SELECT * FROM public.patients")
print(output.fetchall())
conn.close()