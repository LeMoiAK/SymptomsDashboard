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
    return schemas.DailyLogOut.model_validate(db_log)

def get_single_log_per_id(dbSession: Session, log_id: int) -> schemas.DailyLogOut:
    """Gets an existing log in the database by id"""
    # Fetch existing record
    db_log = dbSession.query(models.DailyLog).filter(models.DailyLog.log_id == log_id).first()
    return schemas.DailyLogOut.model_validate(db_log)

def get_single_log_per_patient_date(dbSession: Session, patient_id: int, log_date: date) -> schemas.DailyLogOut:
    """Gets an existing log in the database for a patient and a date"""
    db_log = (
        dbSession.query(models.DailyLog)
        .filter(models.DailyLog.patient_id == patient_id)
        .filter(models.DailyLog.log_date == log_date)
        .first()
    )
    return schemas.DailyLogOut.model_validate(db_log)

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

    return schemas.DailyLogOut.model_validate(db_log)

def get_logs_between_dates_for_patient(dbSession: Session, patient_id: int, start_date: date, end_date: date) -> List[schemas.DailyLogOut]:
    """Gets all the logs between start and end dates (included) for a patient_id"""
    rows = (
        dbSession.query(models.DailyLog)
        .filter(models.DailyLog.patient_id == patient_id)
        .filter(models.DailyLog.log_date >= start_date)
        .filter(models.DailyLog.log_date <= end_date)
        .all()
    )
    return [schemas.DailyLogOut.model_validate(r) for r in rows]

# ------------------- FUNCTIONS FOR THE PATIENTS AND DOCTORS -------------------
def create_patient(dbSession: Session, patient: schemas.PatientCreate) -> schemas.PatientOut:
    """Inserts a new patient into the database"""
    db_patient = models.Patients(**patient.model_dump())
    dbSession.add(db_patient)
    dbSession.commit()
    dbSession.refresh(db_patient)
    return schemas.PatientOut.model_validate(db_patient)

def get_patient_info(dbSession: Session, patient_id: int) -> schemas.PatientOut:
    """Gets the info for a patient"""
    # Fetch existing record
    db_patient = dbSession.query(models.Patients).filter(models.Patients.patient_id == patient_id).first()
    return schemas.PatientOut.model_validate(db_patient)

def get_all_patients(dbSession: Session) -> List[schemas.PatientOut]:
    """Returns the list of all the patients"""
    rows = dbSession.query(models.Patients).all()
    return [schemas.PatientOut.model_validate(r) for r in rows]

def create_doctor(dbSession: Session, doctor: schemas.DoctorCreate) -> schemas.DoctorOut:
    """Inserts a new doctor into the database"""
    db_doctor = models.Doctors(**doctor.model_dump())
    dbSession.add(db_doctor)
    dbSession.commit()
    dbSession.refresh(db_doctor)
    return schemas.DoctorOut.model_validate(db_doctor)

def get_doctor_info(dbSession: Session, doctor_id: int) -> schemas.DoctorOut:
    """Gets the info for a doctor"""
    # Fetch existing record
    db_doctor = dbSession.query(models.Doctors).filter(models.Doctors.doctor_id == doctor_id).first()
    return schemas.DoctorOut.model_validate(db_doctor)

def get_all_doctors(dbSession: Session) -> List[schemas.DoctorOut]:
    """Returns the list of all the doctors"""
    rows = dbSession.query(models.Doctors).all()
    return [schemas.DoctorOut.model_validate(r) for r in rows]

# ------------------- FUNCTIONS FOR THE TREATMENTS -------------------
def create_treatment(dbSession: Session, treatment: schemas.TreatmentCreate) -> schemas.TreatmentOut:
    """Inserts a new treatment into the database"""
    db_treatment = models.Treatment(**treatment.model_dump())
    dbSession.add(db_treatment)
    dbSession.commit()
    dbSession.refresh(db_treatment)
    return schemas.TreatmentOut.model_validate(db_treatment)

def get_treatment_info(dbSession: Session, treatment_id: int) -> schemas.TreatmentOut:
    """Gets the info for a treatment"""
    # Fetch existing record
    db_treatment = dbSession.query(models.Treatment).filter(models.Treatment.treatment_id == treatment_id).first()
    return schemas.TreatmentOut.model_validate(db_treatment)

def get_treatments_between_dates_for_patient(dbSession: Session, patient_id: int, start_date: date, end_date: date) -> List[schemas.TreatmentOut]:
    """Gets all the treatments between start and end dates (included) for a patient_id"""
    rows = (
        dbSession.query(models.Treatment)
        .filter(models.Treatment.patient_id == patient_id)
        .filter(models.Treatment.treatment_date >= start_date)
        .filter(models.Treatment.treatment_date <= end_date)
        .all()
    )
    return [schemas.TreatmentOut.model_validate(r) for r in rows]

def get_last_treatment_for_patient(dbSession: Session, patient_id: int) -> schemas.TreatmentOut:
    """Gets the last treatment for a patient_id"""
    db_treatment = (
        dbSession.query(models.Treatment)
        .filter(models.Treatment.patient_id == patient_id)
        .order_by(models.Treatment.patient_id.desc())
        .first()
    )
    return schemas.TreatmentOut.model_validate(db_treatment)

# ------------------- FUNCTIONS FOR THE APPOINTMENTS -------------------
def create_appointment(dbSession: Session, appointment: schemas.AppointmentCreate) -> schemas.AppointmentOut:
    """Inserts a new appointment into the database"""
    db_appointment = models.Appointments(**appointment.model_dump())
    dbSession.add(db_appointment)
    dbSession.commit()
    dbSession.refresh(db_appointment)
    return schemas.AppointmentOut.model_validate(db_appointment)

def get_appointments_for_patient(dbSession: Session, patient_id: int) -> List[schemas.AppointmentOut]:
    """Gets all appointments for a patient"""
    rows = (
        dbSession.query(models.Appointments)
        .filter(models.Appointments.patient_id == patient_id)
        .all()
    )
    return [schemas.AppointmentOut.model_validate(r) for r in rows]

def get_appointments_for_doctor(dbSession: Session, doctor_id: int) -> List[schemas.AppointmentOut]:
    """Gets all appointments for a patient"""
    rows = (
        dbSession.query(models.Appointments)
        .filter(models.Appointments.doctor_id == doctor_id)
        .all()
    )
    return [schemas.AppointmentOut.model_validate(r) for r in rows]