# app/controllers/usuario_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.repositories.usuario_repository import (
    get_usuarios, get_usuario, crear_usuario, actualizar_usuario,
    desactivar_usuario, eliminar_usuario
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# LIST
@router.get("", status_code=status.HTTP_200_OK)
def listar_usuarios(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    items, total = get_usuarios(db, skip=skip, limit=limit)
    return {
        "total": total,
        "data": [u.to_public_dict() for u in items]
    }

# GET by id
@router.get("/{id}", status_code=status.HTTP_200_OK)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    u = get_usuario(db, id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"data": u.to_public_dict()}

# CREATE
@router.post("", status_code=status.HTTP_201_CREATED)
def crear_usuario_endpoint(body: dict, db: Session = Depends(get_db)):
    # body: {usuario, password, nombre?, correo?, rol?, estado?}
    required = ["usuario", "password"]
    missing = [k for k in required if not body.get(k)]
    if missing:
        raise HTTPException(status_code=400, detail=f"Falta(n): {', '.join(missing)}")

    try:
        creado = crear_usuario(db, body)
    except ValueError as ve:
        raise HTTPException(status_code=409, detail=str(ve))

    return {"message": "Usuario creado exitosamente", "data": creado.to_public_dict()}

# UPDATE (PUT)
@router.put("/{id}", status_code=status.HTTP_200_OK)
def actualizar_usuario_endpoint(id: int, body: dict, db: Session = Depends(get_db)):
    # body: puede contener {usuario?, nombre?, correo?, rol?, estado?, password?}
    try:
        actualizado = actualizar_usuario(db, id, body)
    except ValueError as ve:
        raise HTTPException(status_code=409, detail=str(ve))
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario actualizado", "data": actualizado.to_public_dict()}

# DESACTIVAR (soft delete)
@router.patch("/{id}/desactivar", status_code=status.HTTP_200_OK)
def desactivar_usuario_endpoint(id: int, db: Session = Depends(get_db)):
    ok = desactivar_usuario(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario desactivado"}

# DELETE físico (opcional; si no lo quieres, elimínalo)
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_usuario_endpoint(id: int, db: Session = Depends(get_db)):
    ok = eliminar_usuario(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}
