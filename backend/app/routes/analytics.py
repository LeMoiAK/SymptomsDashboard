from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from ..db import get_db
from ..crud import get_logs_for_week

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/weekly")
def weekly_analytics(start_date: date, db: Session = Depends(get_db)):
    logs = get_logs_for_week(db, start_date)

    days = [(start_date + timedelta(days=i)) for i in range(7)]

    mood_map = {log.date: log.mood for log in logs if log.mood is not None}

    return {
        "dates": [d.isoformat() for d in days],
        "mood": [mood_map.get(d) for d in days],
        "log_count": len(logs),
    }