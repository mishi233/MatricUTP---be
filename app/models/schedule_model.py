from pydantic import BaseModel, Field
from typing import Annotated

class ScheduleDAO(BaseModel):
    id: Annotated[int, Field(...)]
    hour_id: Annotated[int, Field(...)]
    course_id: Annotated[int, Field(...)]