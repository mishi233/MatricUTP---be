from pydantic import BaseModel, Field
from typing import Annotated

class Course(BaseModel):
    id: Annotated[int, Field(...)]
    subject_id: Annotated[str, Field(..., min_length=1, max_length=10)]
    teacher_id: Annotated[int, Field(...)]
    difficulty: Annotated[int, Field(...)]