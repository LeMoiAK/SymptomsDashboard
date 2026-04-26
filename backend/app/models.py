from sqlalchemy import Column, Integer, String, Date, Text
from .db import Base


class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    text = Column(Text, nullable=False)
    mood = Column(Integer, nullable=True)