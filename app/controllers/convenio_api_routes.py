from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.convenio_service import ConvenioService
from app.config.security import get_current_user

router = APIRouter(prefix="/convenios", tags=["Convenios"])
# ---------------------------- CREAR CONVENIO ---------------------------- #
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_convenio(
    convenio_data: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔒 requiere JWT
):
    try:
        convenio = ConvenioService.crear(db, convenio_data)
        return {
            "message": f"Convenio creado correctamente por {current_user['id']}",
            "data": convenio
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------- LISTAR CONVENIOS ---------------------------- #
@router.get("/", status_code=status.HTTP_200_OK)
def listar_convenios(
    skip: int = 0,
    limit: int = 25,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔒 requiere JWT
):
    convenios = ConvenioService.listar(db, skip, limit)
    return {
        "total": len(convenios),
        "usuario": current_user["id"],  # puedes omitirlo si no lo necesitas
        "data": convenios
    }

# ---------------------------- OBTENER CONVENIOS PRO ---------------------------- #

@router.get("/movilidades", status_code=status.HTTP_200_OK)
def listar_convenios_con_movilidades(
    skip: int = 0,
    limit: int = 25,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    convenios = ConvenioService.listar_con_movilidades(db, skip, limit)
    
    # Convertimos a formato JSON amigable
    data = [
        {
            "codigo": c.codigo,
            "nombre": c.nombre_convenio,
            "tipo": c.tipo,
            "fecha_inicio": c.fecha_inicio,
            "fecha_finalizacion": c.fecha_finalizacion,
            "estado": c.estado,
            "nombre_institucion": c.nombre_institucion,
            "Movilidades del convenio": c.movilidades_convenio or []
        }
        for c in convenios
    ]

    return {
        "total": len(data),
        "usuario": current_user["id"],
        "data": data
    }

# ---------------------------- OBTENER POR CÓDIGO ---------------------------- #
@router.get("/{codigo}", status_code=status.HTTP_200_OK)
def obtener_convenio(
    codigo: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔒 requiere JWT
):
    convenio = ConvenioService.obtener_por_codigo(db, codigo)
    if not convenio:
        raise HTTPException(status_code=404, detail="Convenio no encontrado")
    return convenio


# ---------------------------- ACTUALIZAR ---------------------------- #
@router.put("/{codigo}", status_code=status.HTTP_200_OK)
def actualizar_convenio(
    codigo: str,
    updates: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔒 requiere JWT
):
    convenio_actualizado = ConvenioService.actualizar(db, codigo, updates)
    if not convenio_actualizado:
        raise HTTPException(status_code=404, detail="Convenio no encontrado")
    return {
        "message": f"Convenio actualizado correctamente por {current_user['id']}",
        "data": convenio_actualizado
    }


# ---------------------------- ELIMINAR (LÓGICO) ---------------------------- #
@router.delete("/{codigo}", status_code=status.HTTP_200_OK)
def eliminar_convenio(
    codigo: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # 🔒 requiere JWT
):
    exito = ConvenioService.eliminar(db, codigo)
    if not exito:
        raise HTTPException(status_code=404, detail="Convenio no encontrado o ya inactivo")
    return {"message": f"Convenio inactivado correctamente por {current_user['id']}"}