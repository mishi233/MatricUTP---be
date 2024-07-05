from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.repositories.teachers_dao import TeachersDAO
from app.repositories.courses_dao import CourseDAO
from app.repositories.schedule_dao import ScheduleDAO
from app.repositories.hours_dao import HoursDAO
from app.repositories.subject_dao import SubjectDAO
from datetime import datetime
import json
import os

class CursoDisponible():
    def __init__(self, idMateria, horarios, creditos):
        self.__idMateria = idMateria
        self.__horarios = horarios
        self.__creditos = creditos

    @property
    def getIdMateria(self):
        return self.__idMateria

    @property
    def getHorarios(self):
        return self.__horarios
    
    @property
    def getCreditos(self):
        return self.__creditos
    
class GeneralService():

    @staticmethod
    async def is_db_empty(db: AsyncSession) -> bool:
        """
        Verificar si las tablas están vacías.
        """
        teachers_count = await db.scalar(select(func.count(TeachersDAO.id)))
        courses_count = await db.scalar(select(func.count(CourseDAO.id)))
        schedules_count = await db.scalar(select(func.count(ScheduleDAO.id)))
        hours_count = await db.scalar(select(func.count(HoursDAO.id)))
        subjects_count = await db.scalar(select(func.count(SubjectDAO.id)))
        
        return all(count == 0 for count in [teachers_count, courses_count, schedules_count, hours_count, subjects_count])

    @staticmethod
    async def initialize_db(db: AsyncSession):
        """
            Inicializar datos primordiales para el funcionamiento del software.
        """ 
        if not await GeneralService.is_db_empty(db):
            return

        dirActual = os.path.dirname(__file__)
        archivoJson = os.path.join(dirActual, '..', '..', 'materias.json')

        with open(archivoJson, 'r', encoding='utf-8') as file:
            datos = json.load(file)

        profesores = []
        horario = []
        materias = []
        codigos = set()

        for dato in datos:
            if dato['codigo'] not in codigos:
                codigos.add(dato['codigo'])
                materias.append([dato['codigo'], dato['nombre_materia']])

            if dato['profesor'] not in profesores:
                profesores.append(dato['profesor'])

            for horaClase in dato['horario']:
                if horaClase not in horario:
                    horario.append(horaClase)

        for nombreMateria_codigo in materias:
            materia = SubjectDAO(id=nombreMateria_codigo[0], name=nombreMateria_codigo[1])
            db.add(materia)

        for nombreProfesor in profesores:
            teacher = TeachersDAO(name=nombreProfesor)
            db.add(teacher)

        for horaClase in horario:
            dia, hora_str = horaClase.split()
            hora = datetime.strptime(hora_str, "%H:%M").time()
            hours = HoursDAO(dayOfWeek=dia, hour=hora)
            db.add(hours)

        await db.commit()

        for dato in datos:
            
            profesor_id_result  = await db.execute(
                select(TeachersDAO.id)
                .where(TeachersDAO.name == dato['profesor'])
            )
            profesor_id = profesor_id_result .scalar_one_or_none()

            course = CourseDAO(
                subject_id=dato['codigo'],
                teacher_id=profesor_id,
                difficulty=dato['dificultad']
            )
            db.add(course)
            await db.flush()

            course_id = course.id
            for horaClase in dato['horario']:
                dia, hora_str = horaClase.split()
                hora = datetime.strptime(hora_str, "%H:%M").time()
                horario_id_result = await db.execute(
                    select(HoursDAO.id).where(
                        HoursDAO.dayOfWeek == dia,
                        HoursDAO.hour == hora
                    )
                )
                horario_id = horario_id_result.scalar_one_or_none()

                horarioCompleto = ScheduleDAO(hour_id=horario_id, course_id=course_id)
                db.add(horarioCompleto)

            await db.commit()

    async def obtenerInformacionMaterias(self, materia, db: AsyncSession):
        cursos_info = []

        #Obtenemos la información de las materias
        result = await db.execute(
            select(CourseDAO.id, CourseDAO.subject_id, SubjectDAO.name, TeachersDAO.name,  CourseDAO.difficulty)
            .join(CourseDAO, CourseDAO.subject_id == SubjectDAO.id)
            .join(TeachersDAO, TeachersDAO.id == CourseDAO.teacher_id)
            .where(CourseDAO.subject_id == materia)
        )
        cursos = result.fetchall()

        #Obtenemos los horarios de cada materia
        for curso in cursos:
            horario = await db.execute(
                select(HoursDAO.dayOfWeek, HoursDAO.hour)
                .join(ScheduleDAO, ScheduleDAO.hour_id == HoursDAO.id)
                .where(ScheduleDAO.course_id == curso[0])
            )
            horarios = (horario.fetchall())

            curso_info = {
            "teacher_name": curso[3],
            "difficulty": curso[4],
            "horarios": [{"dayOfWeek": h[0], "hour": h[1].strftime("%H:%M")} for h in horarios]
            }

            cursos_info.append(curso_info)

        materias_info = {
            "subject_id": curso[1],
            "subject_name": curso[2],
            "cursos": cursos_info
        }

        return materias_info
    

    #Funciones para generar horario
    def ponerMateriasObligatorias(self, lista):
        codigos = []
        repetidos = []
        for materia in lista:
            if materia.getIdMateria in codigos:
                repetidos.append(materia.getIdMateria)
            else:
                codigos.append(materia.getIdMateria)   

        codigosSinRepetir = []
        for codigo in codigos:
            if codigo not in repetidos:
                codigosSinRepetir.append(codigo)

        horarios = []
        for codigo in codigosSinRepetir:
            for materia in lista:
                if materia.getIdMateria == codigo:
                    horarios.append(materia.getHorarios)
                    break
        
        mejorHorario = self.generarHorario()
        

                

    def crearHorario(self, listaPosibles, listaObligatorias):  
        self.ponerMateriasObligatorias(listaObligatorias)

    