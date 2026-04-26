from pydantic import BaseModel
from datetime import date
from typing import Optional


class DailyLogCreate(BaseModel):
    date: date
    text: str
    mood: Optional[int] = None


class DailyLogOut(BaseModel):
    id: int
    date: date
    text: str
    mood: Optional[int]

    class Config:
        from_attributes = True