from pydantic import BaseModel, Field
from typing import Annotated
from datetime import time

class Hours(BaseModel):
    id: Annotated[int, Field(...)]
    dayOfWeek: Annotated[str, Field(..., min_length=1, max_length=10)]
    hour: Annotated[time, Field(...)]