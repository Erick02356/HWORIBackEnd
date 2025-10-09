from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.convenio_service import ConvenioService

router = APIRouter(prefix="/convenios", tags=["Convenios"])


# Crear un nuevo convenio
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_convenio(convenio_data: dict, db: Session = Depends(get_db)):
    try:
        convenio = ConvenioService.crear(db, convenio_data)
        return {"message": "Convenio creado correctamente", "data": convenio}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Listar convenios activos
@router.get("/", status_code=status.HTTP_200_OK)
def listar_convenios(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    convenios = ConvenioService.listar(db, skip, limit)
    return {"total": len(convenios), "data": convenios}


# Obtener convenio por código
@router.get("/{codigo}", status_code=status.HTTP_200_OK)
def obtener_convenio(codigo: str, db: Session = Depends(get_db)):
    convenio = ConvenioService.obtener_por_codigo(db, codigo)
    if not convenio:
        raise HTTPException(status_code=404, detail="Convenio no encontrado")
    return convenio


# Actualizar convenio
@router.put("/{codigo}", status_code=status.HTTP_200_OK)
def actualizar_convenio(codigo: str, updates: dict, db: Session = Depends(get_db)):
    convenio_actualizado = ConvenioService.actualizar(db, codigo, updates)
    if not convenio_actualizado:
        raise HTTPException(status_code=404, detail="Convenio no encontrado")
    return {"message": "Convenio actualizado correctamente", "data": convenio_actualizado}


# Eliminación lógica (estado → 'Inactivo')
@router.delete("/{codigo}", status_code=status.HTTP_200_OK)
def eliminar_convenio(codigo: str, db: Session = Depends(get_db)):
    exito = ConvenioService.eliminar(db, codigo)
    if not exito:
        raise HTTPException(status_code=404, detail="Convenio no encontrado o ya inactivo")
    return {"message": "Convenio inactivado correctamente"}
