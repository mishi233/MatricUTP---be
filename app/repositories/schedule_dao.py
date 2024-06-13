from db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class ScheduleDAO(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    hour_id = Column(Integer, ForeignKey('hours.id'), nullable=False) 
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False) 

    hour = relationship("HoursDAO", back_populates="schedules")
    course = relationship("CourseDAO", back_populates="schedules")