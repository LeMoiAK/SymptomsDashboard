"""
The summary service contains a collection of functions to generate a summary of daily logs using an LLM.

The process is:
1. Get logs for the patient in the requested range
2. Get all treatments for that patient
3. For each log, we get if within a cycle and what day of the cycle that is
4. We generate a context to give the LLM and to summarise
5. We call the LLM to get the summary
"""

from datetime import date, timedelta
from typing import List
from sqlalchemy.orm import Session

from .. import crud, schemas

def get_logs_and_format(patient_id: int, start_date: date, end_date: date, db: Session) -> List[dict]:
    """Gets the logs from the db and formats each of them to get ready for the LLM"""

    # Get the logs
    logs = crud.get_logs_between_dates_for_patient(db, patient_id, start_date, end_date)
    if logs is None:
        raise ValueError(f"No logs for this period for patient {patient_id} ({start_date} to {end_date})")
    
    # Get the treatments, assume the earlist treatment to be 2 months before the start_date
    # treatments normally last up to 1 month cycle
    treatment_start_date = start_date - timedelta(days=62)
    treatments = crud.get_treatments_between_dates_for_patient(db, patient_id, treatment_start_date, end_date)
    
    # Now for each day, we get if it is within a cycle
    

def summarize(self, logs: list[str]) -> str:
    # Replace with real LLM call later
    joined = "\n".join(logs)

    return f"Summary of the week:\n\n{joined[:300]}..."