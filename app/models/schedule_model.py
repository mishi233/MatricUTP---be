from pydantic import BaseModel, Field
from typing import Annotated
from typing import List, Any, Dict

class ScheduleDAO(BaseModel):
    id: Annotated[int, Field(...)]
    hour_id: Annotated[int, Field(...)]
    course_id: Annotated[int, Field(...)]

class MateriaList(BaseModel):
    materias: List[str]

class Horario(BaseModel):
    dayOfWeek: str
    hour: str

class Curso(BaseModel):
    teacher_name: str
    horarios: List[Horario]
    opcion: int

class Materia(BaseModel):
    subject_id: str
    subject_name: str
    cursos: List[Curso]

class ListaMateriasCompletas(BaseModel):
    materiasCompletas: List[Materia]

