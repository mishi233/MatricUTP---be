from mimetypes import guess_extension
from typing import Optional
from app.services.general_service import GeneralService
from app.utils.class_utils import Injectable, inject
from app.utils.db_utils import get_db_session
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session
import re


@inject(GeneralService)
class BookController(Injectable):
    def __init__(self):
        self.route = APIRouter(prefix='/book')
        self.route.add_api_route("/search", self.search_books, methods=["GET"])
    
    async def search_books(self, q: str = Query(..., min_length=3, max_length=50), db: Session = Depends(get_db_session)):
        books = await self.bookservice.book_search(db, q)
        
        if books:
            return {"success": True, "results": books}
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No se encontraron resultados.")