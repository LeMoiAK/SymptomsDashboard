from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from ..dbconn import get_db
from ..services.summary import get_summary_between_dates_for_patient

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary_for_patient_between_dates", response_model=str)
def get_summary_for_patient_between_dates(patient_id: int, start_date: date, end_date: date,  db: Session = Depends(get_db)):
    """Gets the summary of daily logs between two dates for a patient"""
    summary = get_summary_between_dates_for_patient(patient_id, start_date, end_date, db)
    return summary