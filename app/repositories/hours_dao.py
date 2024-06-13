from db.base_class import Base
from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship

class HoursDAO(Base):
    __tablename__ = "hours"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    dayOfWeek = Column(String(10), unique=True, nullable=False)
    hour = Column(Time, nullable=False)
    
    schedules = relationship("ScheduleDAO", back_populates="hour")