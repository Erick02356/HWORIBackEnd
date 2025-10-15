from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.institucion_service import InstitucionService

router = APIRouter(prefix="/instituciones", tags=["Instituciones"])

@router.get("/", status_code=status.HTTP_200_OK)
def listar_instituciones(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    instituciones = InstitucionService.listar(db, skip, limit)
    data = [
        {           
            "codigo": i.codigo,
            "nombre": i.nombre,
            "direccion": i.direccion,
            "representante_legal": i.representante_legal,
            "correo": i.correo,
            "telefono": i.telefono,
            "estado": i.estado,
            "codigo_pais": i.codigo_pais,
            "nombre_pais": i.nombre_pais
        }
        for i in instituciones
    ]
    return {"total": len(data), "data": data}


@router.get("/{codigo}", status_code=status.HTTP_200_OK)
def obtener_institucion(codigo: str, db: Session = Depends(get_db)):
    institucion = InstitucionService.obtener_por_codigo(db, codigo)
    if not institucion:
        return {"message": "Institución no encontrada"}
    
    return {
        "data": {
            "codigo": institucion.codigo,
            "nombre": institucion.nombre,
            "direccion": institucion.direccion,
            "representante_legal": institucion.representante_legal,
            "correo": institucion.correo,
            "telefono": institucion.telefono,
            "estado": institucion.estado,
            "codigo_pais": institucion.codigo_pais,
            "nombre_pais": institucion.nombre_pais
        }
    }

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
