from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date, timedelta


def create_log(db: Session, log: schemas.DailyLogCreate):
    db_log = models.DailyLog(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_logs_for_week(db: Session, start_date: date):
    end_date = start_date + timedelta(days=6)

    return (
        db.query(models.DailyLog)
        .filter(models.DailyLog.date >= start_date)
        .filter(models.DailyLog.date <= end_date)
        .all()
    )