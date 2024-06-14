from app.services.general_service import GeneralService
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.utils.db_utils import get_db_session
from app.models.schedule_model import MateriaList

class Controller:
    def __init__(self):
        self.route = APIRouter(prefix='/materia')
        self.route.add_api_route("/obtener", self.obtener_materias, methods=["POST"])
    
    async def obtener_materias(self, lista_materias: MateriaList, db: Session = Depends(get_db_session)):
        materias = lista_materias.materias
        print(materias)
        result = True
        #result = await self.book_service.procesar_materias(db, materias)
        
        if result:
            return {"success": True, "results": result}
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No se encontraron resultados.")
