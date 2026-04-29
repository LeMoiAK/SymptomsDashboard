"""
The patients sub-section of APIs contains all the functions to create,
and get patients from the database
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from .. import crud, schemas
from ..dbconn import get_db

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/create", response_model=schemas.PatientOut)
def create_log(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """Inserts a new patient in the database and returns the created one with its id"""
    return crud.create_patient(db, patient)

@router.get("/get_single_per_id", response_model=schemas.PatientOut)
def get_single_per_id(patient_id: int, db: Session = Depends(get_db)):
    """Gets a single patient by id"""
    return crud.get_patient_info(db, patient_id)

@router.get("/get_all", response_model=List[schemas.PatientOut])
def get_all_patients(db: Session = Depends(get_db)):
    """Gets all patients"""
    return crud.get_all_patients(db)