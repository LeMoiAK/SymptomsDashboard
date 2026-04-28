"""
The schemas module contains schemas of the data used in the backend using Pydantic for data validation.
"""

from pydantic import BaseModel
from datetime import date
from typing import Optional


class DailyLogCreate(BaseModel):
    """A log before going into the database, so no log_id"""
    patient_id: int
    log_date: date
    log_text: Optional[str] = None
    symptom_Pain: int
    symptom_Fatigue: int
    symptom_Diarrhea: int
    symptom_Nausea: int

class DailyLogOut(BaseModel):
    """A log after going into the database, so with log_id"""
    log_id: int
    patient_id: int
    log_date: date
    log_text: Optional[str] = None
    symptom_Pain: int
    symptom_Fatigue: int
    symptom_Diarrhea: int
    symptom_Nausea: int

    class Config:
        from_attributes = True