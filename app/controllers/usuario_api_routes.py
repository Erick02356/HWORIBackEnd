from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.UsuarioModel import Usuario
from app.repositories.usuario_repository import (
    get_usuarios, get_usuario, crear_usuario, eliminar_usuario
)

router = APIRouter()

@router.get("/usuarios")
def listar_usuarios(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    usuarios = get_usuarios(db, skip=skip, limit=limit)
    return {"usuarios": usuarios}

@router.get("/usuarios/{id}")
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = get_usuario(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios")
def crear_usuario_endpoint(nombres: str, apellidos: str, email: str, password: str, rol: str, db: Session = Depends(get_db)):
    nuevo = Usuario(nombres=nombres, apellidos=apellidos, email=email, password=password, rol=rol)
    creado = crear_usuario(db, nuevo)
    return {"message": "Usuario creado exitosamente", "usuario": creado}

@router.delete("/usuarios/{id}")
def eliminar_usuario_endpoint(id: int, db: Session = Depends(get_db)):
    exito = eliminar_usuario(db, id)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Eliminado exitosamente"}
