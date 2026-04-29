"""
The doctors sub-section of APIs contains all the functions to create,
and get doctors from the database
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from .. import crud, schemas
from ..dbconn import get_db

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.post("/create", response_model=schemas.DoctorOut)
def create_log(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """Inserts a new doctor in the database and returns the created one with its id"""
    return crud.create_doctor(db, doctor)

@router.get("/get_single_per_id", response_model=schemas.DoctorOut)
def get_single_per_id(doctor_id: int, db: Session = Depends(get_db)):
    """Gets a single doctor by id"""
    return crud.get_doctor_info(db, doctor_id)

@router.get("/get_all", response_model=List[schemas.DoctorOut])
def get_all_doctors(db: Session = Depends(get_db)):
    """Gets all doctors"""
    return crud.get_all_doctors(db)