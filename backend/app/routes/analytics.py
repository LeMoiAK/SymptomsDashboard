from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from ..dbconn import get_db
from ..crud import get_logs_between_dates_for_patient

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/weekly")
def weekly_analytics(start_date: date, db: Session = Depends(get_db)):
    """Obtains all logs for a week after the start date"""
    end_date = start_date + timedelta(days=6)
    logs = get_logs_between_dates_for_patient(db, start_date, end_date)

    days = [(start_date + timedelta(days=i)) for i in range(7)]

    pain_map = {log.log_date: log.symptom_Pain for log in logs if log.symptom_Pain is not None}

    return {
        "dates": [d.isoformat() for d in days],
        "pain": [pain_map.get(d) for d in days],
        "log_count": len(logs),
    }