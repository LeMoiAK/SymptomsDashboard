"""
The crud module contains all functions to interact with the database.
CREATE, READ, UPDATE, DELETE
"""

from sqlalchemy.orm import Session
import sqlalchemy as db
from . import models, schemas
from datetime import date, timedelta
from typing import List

# ------------------- FUNCTIONS FOR THE DAILY LOGS -------------------
def create_log(dbSession: Session, log: schemas.DailyLogCreate) -> schemas.DailyLogOut:
    """Inserts a new log into the database"""
    db_log = models.DailyLog(**log.model_dump())
    dbSession.add(db_log)
    dbSession.commit()
    dbSession.refresh(db_log)
    return db_log

def get_single_log_per_id(dbSession: Session, log_id: int) -> schemas.DailyLogOut:
    """Gets an existing log in the database by id"""
    # Fetch existing record
    db_log = dbSession.query(models.DailyLog).filter(models.DailyLog.log_id == log_id).first()

    return db_log

def get_single_log_per_patient_date(dbSession: Session, patient_id: int, log_date: date) -> schemas.DailyLogOut:
    """Gets an existing log in the database for a patient and a date"""
    return (
        dbSession.query(models.DailyLog)
        .filter(models.DailyLog.patient_id == patient_id)
        .filter(models.DailyLog.log_date == log_date)
        .first()
    )

def update_log(dbSession: Session, log: schemas.DailyLogOut) -> schemas.DailyLogOut:
    """Updates an existing log in the database"""
    # 1. Fetch existing record
    db_log = get_single_log_per_id(dbSession, log.log_id)

    if not db_log:
        raise ValueError(f"Log with id {log.log_id} not found")

    # 2. Update fields
    update_data = log.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_log, field, value)

    # 3. Commit changes
    dbSession.commit()
    dbSession.refresh(db_log)

    return db_log

def get_logs_between_dates_for_patient(dbSession: Session, patient_id: int, start_date: date, end_date: date) -> List[schemas.DailyLogOut]:
    """Gets all the logs between start and end dates (included) for a patient_id"""
    return (
        dbSession.query(models.DailyLog)
        .filter(models.DailyLog.patient_id == patient_id)
        .filter(models.DailyLog.log_date >= start_date)
        .filter(models.DailyLog.log_date <= end_date)
        .all()
    )

# ------------------- FUNCTIONS FOR THE PATIENTS AND DOCTORS -------------------
def create_patient(dbSession: Session, patient: schemas.PatientCreate) -> schemas.PatientOut:
    """Inserts a new patient into the database"""
    db_patient = models.Patients(**patient.model_dump())
    dbSession.add(db_patient)
    dbSession.commit()
    dbSession.refresh(db_patient)
    return db_patient

def get_patient_info(dbSession: Session, patient_id: int) -> schemas.PatientOut:
    """Gets the info for a patient"""
    # Fetch existing record
    return dbSession.query(models.Patients).filter(models.Patients.patient_id == patient_id).first()

def get_all_patients(dbSession: Session) -> List[schemas.PatientOut]:
    """Returns the list of all the patients"""
    return dbSession.query(models.Patients).all()

def create_doctor(dbSession: Session, doctor: schemas.DoctorCreate) -> schemas.DoctorOut:
    """Inserts a new doctor into the database"""
    db_doctor = models.Doctors(**doctor.model_dump())
    dbSession.add(db_doctor)
    dbSession.commit()
    dbSession.refresh(db_doctor)
    return db_doctor

def get_doctor_info(dbSession: Session, doctor_id: int) -> schemas.DoctorOut:
    """Gets the info for a doctor"""
    # Fetch existing record
    return dbSession.query(models.Doctors).filter(models.Doctors.doctor_id == doctor_id).first()

def get_all_doctors(dbSession: Session) -> List[schemas.DoctorOut]:
    """Returns the list of all the doctors"""
    return dbSession.query(models.DoctorOut).all()