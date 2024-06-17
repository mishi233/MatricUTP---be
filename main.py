from app.controllers.general_controller import Controller
from app.services.general_service import GeneralService
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.connection import engine
from app.utils.db_utils import create_tables, get_db_session
import uvicorn, os

class ServerBootstrap:
    origin = [ os.getenv("CORS_ORIGIN") ]
    
    def __init__(self, app: FastAPI):
        generalController = Controller()

        self.app = app
        self.HOST = os.getenv("HOST")
        self.app.include_router(generalController.route, prefix='/api') 

    def run(self):
        uvicorn.run(self.app, host=self.HOST, port=8000)        
    
    @staticmethod
    @asynccontextmanager
    async def start_up_events(app: FastAPI):
        # Crear las tablas en la base de datos
        await create_tables(engine)

        async for session in get_db_session():
            try:
                await GeneralService.initialize_db(session)
            finally:
                await session.close()
                
        yield
    
def main():
    app = FastAPI(lifespan=ServerBootstrap.start_up_events)
    app.add_middleware(CORSMiddleware, 
                        allow_origins=ServerBootstrap.origin,
                        allow_credentials=True, 
                        allow_methods=["*"],
                        allow_headers=["*"])
    ServerBootstrap(app).run()

if __name__ == "__main__":
    main()