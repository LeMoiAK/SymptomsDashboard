"""
The models module contains all the database tables models.
"""

import sqlalchemy as db
from .dbconn import BaseModel


class Patients(BaseModel):
    """The patients table"""
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True, index=True)
    patient_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    NHS_number = db.Column(db.String(10), nullable=False)

class Doctors(BaseModel):
    """The doctors table"""
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, index=True)
    doctor_name = db.Column(db.String(100), nullable=False)

class DailyLog(BaseModel):
    """Daily logs recorded by patients"""
    __tablename__ = "daily_log"

    log_id = db.Column(db.Integer, primary_key=True, index=True)
    patient_id = db.Column(db.Integer, nullable=False)
    log_date = db.Column(db.Date, nullable=False)
    log_text = db.Column(db.Text)
    symptom_Pain = db.Column(db.Integer, nullable=False)
    symptom_Fatigue = db.Column(db.Integer, nullable=False)
    symptom_Diarrhea = db.Column(db.Integer, nullable=False)
    symptom_Nausea = db.Column(db.Integer, nullable=False)

class Appointments(BaseModel):
    """Appointments between doctor and patient"""
    __tablename__ = "appointments"

    appt_id = db.Column(db.Integer, primary_key=True, index=True)
    appt_date = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)

class Treatment(BaseModel):
    """The treatments given to a patient"""
    __tablename__ = "treatments"

    treatment_id = db.Column(db.Integer, primary_key=True, index=True)
    treatment_date = db.Column(db.Date, nullable=False)
    patient_id = db.Column(db.Integer, nullable=False)
    cycle_number = db.Column(db.Integer, nullable=False)
    cycle_duration = db.Column(db.Integer, nullable=False)
    drug = db.Column(db.Text)