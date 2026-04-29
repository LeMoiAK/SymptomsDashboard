"""
The logs sub-section of APIs contains all the functions to create,
update, and get logs from the database
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from .. import crud, schemas
from ..dbconn import get_db

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post("/create", response_model=schemas.DailyLogOut)
def create_log(log: schemas.DailyLogCreate, db: Session = Depends(get_db)):
    """Inserts a new log in the database and returns the created one with its id"""
    return crud.create_log(db, log)

@router.put("/update_log", response_model=schemas.DailyLogOut)
def update_log(log: schemas.DailyLogOut,  db: Session = Depends(get_db)):
    """Update a single log"""
    return crud.update_log(db, log)

@router.get("/get_single_per_id", response_model=schemas.DailyLogOut)
def get_log(log_id: int, db: Session = Depends(get_db)):
    """Gets a single log by id"""
    return crud.get_single_log_per_id(db, log_id)

@router.get("/get_single_per_patient_date", response_model=schemas.DailyLogOut)
def get_log(patient_id: int, log_date: date,  db: Session = Depends(get_db)):
    """Gets a single log by patient_id and date"""
    return crud.get_single_log_per_patient_date(db, patient_id, log_date)

@router.get("/get_between_dates_for_patient", response_model=List[schemas.DailyLogOut])
def get_log(patient_id: int, start_date: date, end_date: date,  db: Session = Depends(get_db)):
    """Gets a single log by patient_id and date"""
    return crud.get_logs_between_dates_for_patient(db, patient_id, start_date, end_date)
