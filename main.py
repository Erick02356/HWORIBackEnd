# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.services.PostgresqlConexion import Postgresql
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    Postgresql.iniciar_pool()
    yield
    Postgresql.cerrar_pool()

app = FastAPI(lifespan=lifespan)
load_dotenv()



#routes auth
from app.controllers import auth_api_routes
app.include_router(auth_api_routes.router, prefix="/api")

#routes usuario
from app.controllers import usuario_api_routes
app.include_router(usuario_api_routes.router, prefix="/api")

#routes programa academico
from app.controllers import programa_academico_api_routes
app.include_router(programa_academico_api_routes.router, prefix="/api")


