from db.base_class import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class TeachersDAO(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(45), unique=True, nullable=False)

    courses = relationship("CourseDAO", back_populates="teacher")