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
from .llm import summarise_logs_pipeline

# ----------------------------- FUNCTIONS TO INTERROGATE DB -----------------------------
def get_logs_and_format(patient_id: int, start_date: date, end_date: date, db: Session) -> List[schemas.DailyLogOut]:
    """Gets the logs from the db and formats each of them to get ready for the LLM"""

    # Get the logs
    logs = crud.get_logs_between_dates_for_patient(db, patient_id, start_date, end_date)
    if logs is None:
        raise ValueError(f"No logs for this period for patient {patient_id} ({start_date} to {end_date})")
    
    # Get the treatments, assume the earlist treatment to be 2 months before the start_date
    # treatments normally last up to 1 month cycle
    # It's possible there are no treatments yet
    treatment_start_date = start_date - timedelta(days=62)
    treatments = crud.get_treatments_between_dates_for_patient(db, patient_id, treatment_start_date, end_date)
    
    # Now for each day, we get if it is within a cycle and adapt the log text with info
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
        final_log_text = f"{log_date_str} - {treatment_str}"
        if log.log_text and log.log_text != "":
            final_log_text += f" - {log.log_text}"
        # Then add symptoms level
        final_log_text += f"\nSymptom levels: Pain={log.symptom_Pain}/4 | Fatigue={log.symptom_Fatigue}/4 | Diarrhea={log.symptom_Diarrhea}/4 | Nausea={log.symptom_Nausea}/4"
        # Then replace it
        log.log_text = final_log_text

    return logs 


# ----------------------------- FUNCTIONS TO RUN THE WHOLE PIPELINE -----------------------------
def get_summary_between_dates_for_patient(patient_id: int, start_date: date, end_date: date, db: Session) -> str:
    """
    Gets the logs from the db then summarises them using the LLM.
    """

    # Get logs
    daily_logs = get_logs_and_format(patient_id, start_date, end_date, db)

    # Get summary with the LLM
    summary = summarise_logs_pipeline([log.log_text for log in daily_logs], batch_size=14)

    return summary