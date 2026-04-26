from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/logs", tags=["logs"])


@router.post("/", response_model=schemas.DailyLogOut)
def create_log(log: schemas.DailyLogCreate, db: Session = Depends(get_db)):
    return crud.create_log(db, log)