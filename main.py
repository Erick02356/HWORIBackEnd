from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import usuario_api_routes, auth_api_routes, institucion_api_routes, convenio_api_routes, carga_api_routes, utils_api_routes
from app.config.database import Base, engine
from app.config.security import get_current_user

# 🔹 Crear las tablas en la BD si no existen (opcional)
Base.metadata.create_all(bind=engine)

# 🔹 Inicializar la app
app = FastAPI(title="API de Convenios", version="1.0")

# 🔹 Configurar CORS (puedes ajustar los orígenes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o lista específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Registrar routers
app.include_router(usuario_api_routes.router, prefix="/api", tags=["Usuarios"],  dependencies=[Depends(get_current_user)])
app.include_router(auth_api_routes.router, prefix="/api", tags=["Autenticación"])
app.include_router(institucion_api_routes.router, prefix="/api", tags=["Instituciones"],  dependencies=[Depends(get_current_user)])
app.include_router(convenio_api_routes.router, prefix="/api", tags=["Convenios"])
app.include_router(carga_api_routes.router, prefix="/api", tags=["Ingesta"])
app.include_router(utils_api_routes.router, prefix="/api", tags=["Utils"])

# Ruta base
@app.get("/")
def root():
    return {"message": "Servidor activo"}
