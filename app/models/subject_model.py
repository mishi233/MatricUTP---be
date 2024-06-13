from pydantic import BaseModel, Field
from typing import Annotated

class Subject(BaseModel):
    id: Annotated[str, Field(..., min_length=1, max_length=10)]
    name: Annotated[str, Field(..., min_length=1, max_length=45)]