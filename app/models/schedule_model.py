from pydantic import BaseModel, Field
from typing import Annotated
from typing import List

class ScheduleDAO(BaseModel):
    id: Annotated[int, Field(...)]
    hour_id: Annotated[int, Field(...)]
    course_id: Annotated[int, Field(...)]

class MateriaList(BaseModel):
    materias: List[str]