from db.base_class import Base
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

class CourseDAO(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    subject_id = Column(String(10), ForeignKey('subject.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    difficulty = Column(Integer, nullable=False)

    subject = relationship("SubjectDAO", back_populates="courses")
    teacher = relationship("TeachersDAO", back_populates="courses")
    schedules = relationship("ScheduleDAO", back_populates="course")