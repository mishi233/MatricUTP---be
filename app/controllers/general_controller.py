from app.services.general_service import GeneralService, CursoDisponible
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.utils.db_utils import get_db_session
from app.models.schedule_model import MateriaList, ListaMateriasCompletas


class Controller:
    def __init__(self):
        self.route = APIRouter(prefix='/materia')
        self.generalService = GeneralService()
        self.route.add_api_route("/obtener", self.obtener_materias, methods=["POST"])
        self.route.add_api_route("/horario", self.generar_horario, methods=["POST"])
    
    async def obtener_materias(self, lista_materias: MateriaList, db: Session = Depends(get_db_session)):
        materias = lista_materias.materias
        if not materias:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No se encontraron resultados.") 

        resultados = []
        for codigo in materias:
            resultado = (await self.generalService.obtenerInformacionMaterias(codigo, db))
            resultados.append(resultado)  

        if resultados:
            return {"success": True, "results": resultados}
        
    async def generar_horario(self, lista_horarios: ListaMateriasCompletas, db: Session = Depends(get_db_session)):
        materiasObligatorias = []
        materiasPosibles = []

        for materia in lista_horarios.materiasCompletas:
            for curso in materia.cursos:
                horarioLista = []
                for horario in curso.horarios:
                    horarioLista.append([horario.dayOfWeek, horario.hour])
                if curso.opcion == 1:
                    materiasObligatorias.append(CursoDisponible(idMateria=materia.subject_id, horarios=horarioLista, creditos=materia.subject_id[-1]))
                else:
                    materiasPosibles.append(CursoDisponible(idMateria=materia.subject_id, horarios=horarioLista, creditos=materia.subject_id[-1]))

        self.generalService.crearHorario(materiasPosibles, materiasObligatorias)