from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import usuario_api_routes, auth_api_routes
from app.config.database import Base, engine

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
app.include_router(usuario_api_routes.router, prefix="/api", tags=["Usuarios"])
app.include_router(auth_api_routes.router, prefix="/api", tags=["Autenticación"])

# 🔹 Ruta base
@app.get("/")
def root():
    return {"message": "Servidor activo"}
