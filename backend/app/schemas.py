"""
The schemas module contains schemas of the data used in the backend using Pydantic for data validation.
"""

from pydantic import BaseModel
from datetime import date
from typing import Optional

# ----- Models for the logs
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

# ----- Models for the Patients
class PatientCreate(BaseModel):
    """A patient info before going into the database"""
    patient_name: str
    date_of_birth: date
    NHS_number: str

class PatientOut(BaseModel):
    """A patient info from the database"""
    patient_id: int
    patient_name: str
    date_of_birth: date
    NHS_number: str

    class Config:
        from_attributes = True

# ----- Models for the Doctors
class DoctorCreate(BaseModel):
    """A doctor info before going into the database"""
    doctor_name: str
class DoctorOut(BaseModel):
    """A doctor info from the database"""
    doctor_id: int
    doctor_name: str

    class Config:
        from_attributes = True