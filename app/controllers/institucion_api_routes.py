from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.institucion_service import InstitucionService

router = APIRouter(prefix="/instituciones", tags=["Instituciones"])

@router.get("/")
def listar_instituciones(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    return InstitucionService.listar(db, skip, limit)

@router.get("/{codigo}")
def obtener_institucion(codigo: str, db: Session = Depends(get_db)):
    institucion = InstitucionService.obtener_por_codigo(db, codigo)
    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return institucion

@router.post("/")
def crear_institucion(data: dict, db: Session = Depends(get_db)):
    return InstitucionService.crear(db, data)

@router.put("/{codigo}")
def actualizar_institucion(codigo: str, data: dict, db: Session = Depends(get_db)):
    institucion = InstitucionService.actualizar(db, codigo, data)
    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return institucion

@router.delete("/{codigo}")
def eliminar_institucion(codigo: str, db: Session = Depends(get_db)):
    eliminado = InstitucionService.eliminar(db, codigo)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return {"message": "Institución eliminada correctamente"}
