from db.base_class import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class SubjectDAO(Base):
    __tablename__ = "subject"

    id = Column(String(10), primary_key=True, unique=True, nullable=False)
    name = Column(String(45), unique=True, nullable=False)

    courses = relationship("CourseDAO", back_populates="subject")
