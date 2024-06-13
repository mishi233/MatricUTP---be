from pydantic import BaseModel, Field
from typing import Annotated

class TeacherDAO(BaseModel):
    id: Annotated[int, Field(...)]
    name: Annotated[str, Field(..., min_length=1, max_length=45)]