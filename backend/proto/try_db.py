"""
Script to experiment with connecting to the PostgreSQL database and run requests.
"""

from app.dbconn import SessionLocal, BaseDeclarativeClass, engine
import app.crud as crud
from sqlalchemy.orm import Session
from datetime import date, timedelta

# Get env vars using pydantic
from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class DbConfig(BaseSettings):
    APP_DB_USER: str = Field(min_length=1)
    APP_DB_PASSWORD: str = Field(min_length=1)
    DATABASE_URL: str = Field(min_length=1)

config = DbConfig()

# Then connect to DB
print(f"URL: {config.DATABASE_URL}")

if __name__ == "__main__":
    db: Session = SessionLocal()

    # Get the logs
    patient_id = 1
    start_date=date(2026, 4, 15)
    end_date=date(2026, 5, 4)
    logs = crud.get_logs_between_dates_for_patient(db, patient_id=patient_id, start_date=start_date, end_date=end_date)
    print(logs)

    # Get the treatments, assume the earlist treatment to be 2 months before the start_date
    # treatments normally last up to 1 month cycle
    treatment_start_date = start_date - timedelta(days=62)
    treatments = crud.get_treatments_between_dates_for_patient(db, patient_id, treatment_start_date, end_date)
    print(treatments)


    # For each log, we find if in a treatment period
    for log in logs:
        log_date = log.log_date

        # Find the treatment with the closest date before that log
        potential_days_in_cycle = [(log_date - t.treatment_date).days for t in treatments]
        valid_indices = [i for i, v in enumerate(potential_days_in_cycle) if v >= 0]
        min_index = (
            min(valid_indices, key=potential_days_in_cycle.__getitem__)
            if valid_indices else None
        )
        # Generate the text for that treatment time
        treatment_str = ""
        if min_index:
            last_treatment = treatments[min_index]
            # Verify if in a cycle or not
            days_since_last_treatment = (log_date - last_treatment.treatment_date).days
            if (days_since_last_treatment + last_treatment.day_in_cycle) > last_treatment.cycle_duration:
                # Not a treatment - gives days since last treatment
                treatment_str = f"{days_since_last_treatment} Days since last treatment"
            else:
                treatment_str = f"treatment Cycle {last_treatment.cycle_number} Day {days_since_last_treatment + last_treatment.day_in_cycle}"
        else:
            # No treatment found, could be logs before starting any cycle
            treatment_str = "No treatment yet"

        # Complete the log text with date, cycle and treatments
        log_date_str = log_date.strftime("%Y-%m-%d")
        final_log_text = f"{log_date_str} - {treatment_str} - {log.log_text}"
        # Then replace it
        log.log_text = final_log_text


    
    print(logs)
    print(logs[0])