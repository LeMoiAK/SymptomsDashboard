"""
The treatments sub-section of APIs contains all the functions to create,
and get treatments from the database
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from .. import crud, schemas
from ..dbconn import get_db

router = APIRouter(prefix="/treatments", tags=["treatments"])

@router.post("/create", response_model=schemas.TreatmentOut)
def create_treatment(treatment: schemas.TreatmentCreate, db: Session = Depends(get_db)):
    """Inserts a new treatment in the database and returns the created one with its id"""
    return crud.create_treatment(db, treatment)

@router.get("/get_single_per_id", response_model=schemas.TreatmentOut)
def get_single_per_id(treatment_id: int, db: Session = Depends(get_db)):
    """Gets a single treatment by id"""
    return crud.get_treatment_info(db, treatment_id)

@router.get("/get_between_dates_for_patient", response_model=List[schemas.TreatmentOut])
def get_treatments_per_patient_between_dates(patient_id: int, start_date: date, end_date: date,  db: Session = Depends(get_db)):
    """Gets all treatments for a patient_id between date"""
    return crud.get_treatments_between_dates_for_patient(db, patient_id, start_date, end_date)

@router.get("/get_last_for_patient", response_model=schemas.TreatmentOut)
def get_treatments_per_patient_between_dates(patient_id: int, db: Session = Depends(get_db)):
    """Gets the last treatment for a patient"""
    return crud.get_last_treatment_for_patient(db, patient_id)