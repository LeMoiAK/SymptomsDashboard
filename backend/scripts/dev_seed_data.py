"""
Populates the db with dev data for testing and debugging.
Load data from csv files and uploads them to the db using CRUD module.
"""

import app.models as models
from app.dbconn import SessionLocal, BaseDeclarativeClass, engine
from sqlalchemy.orm import Session
import pandas as pd
from pathlib import Path
from typing import List

from datetime import date

def insert_csv_into_db(file_path: str, dbModel: BaseDeclarativeClass, date_cols: List[str] = [], batch_size: int = 1000):
    """Inserts a CSV file content to the db."""
    print(f"Starting with {dbModel}")
    session = SessionLocal()

    # Avoid duplicates
    if session.query(dbModel).first():
        print(f"Data for {dbModel} already exists, skipping seed.")
        return
    else:
        print(f"Starting to seed the data for {dbModel}")

    # Load CSV into DataFrame
    df = pd.read_csv(file_path)

    for col in date_cols:
        # Parse to pandas datetime
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Replace NaN with None for SQLAlchemy compatibility
    df = df.where(pd.notnull(df), None)

    records = df.to_dict(orient="records")

    print(f"Adding {len(records)} rows to {dbModel}")

    batch = []
    for row in records:
        obj = dbModel(**row)  # keys must match model columns
        batch.append(obj)

        if len(batch) >= batch_size:
            session.bulk_save_objects(batch)
            session.commit()
            batch.clear()

    if batch:
        session.bulk_save_objects(batch)
        session.commit()

    session.close()
    
    print(f"Done adding rows to {dbModel}")

def seed():
    """Read csv files and populate the db with it"""
    db: Session = SessionLocal()

    # Create tables (dev only; use migrations later)
    BaseDeclarativeClass.metadata.create_all(bind=engine)

    insert_csv_into_db(Path("dev_data/patients.csv"), models.Patients, ["date_of_birth"])
    insert_csv_into_db(Path("dev_data/doctors.csv"), models.Doctors)
    insert_csv_into_db(Path("dev_data/treatments.csv"), models.Treatment, ["treatment_date"])
    insert_csv_into_db(Path("dev_data/appointments.csv"), models.Appointments, ["appt_date"])
    insert_csv_into_db(Path("dev_data/daily_logs.csv"), models.DailyLog, ["log_date"])

    print("Seed data inserted.")

if __name__ == "__main__":
    print("Starting to seed the data into the db")
    seed()