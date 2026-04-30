"""
The appointments sub-section of APIs contains all the functions to create,
and get appointments from the database
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from .. import crud, schemas
from ..dbconn import get_db

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/create", response_model=schemas.AppointmentOut)
def create_treatment(apointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    """Inserts a new appointment in the database and returns the created one with its id"""
    return crud.create_appointment(db, apointment)

@router.get("/get_all_for_patient", response_model=List[schemas.AppointmentOut])
def get_appointments_for_patient(patient_id: int, db: Session = Depends(get_db)):
    """Gets all appointments for a patient_id"""
    return crud.get_appointments_for_patient(db, patient_id)

@router.get("/get_all_for_doctor", response_model=List[schemas.AppointmentOut])
def get_appointments_for_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Gets all appointments for a doctor_id"""
    return crud.get_appointments_for_doctor(db, doctor_id)