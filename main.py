from fastapi.staticfiles import StaticFiles
from app.controllers.user_controller import UserController
from app.utils.class_utils import inject
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, os

@inject(UserController)
class ServerBootstrap:
    """
        ServerBootstrap es responsable de inicializar el servidor.
        Se encarga de inicializar la aplicación de FastAPI y de inicializar los controladores.

        Los controladores son clases que se encargan de manejar las peticiones HTTP.
    """
    origin = [ os.getenv("CORS_ORIGIN") ]
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.HOST = os.getenv("HOST")
        self.app.include_router(self.usercontroller.route, prefix='/api') 

    def run(self):
        uvicorn.run(self.app, host=self.HOST, port=8000)
    
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