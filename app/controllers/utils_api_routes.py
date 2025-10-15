from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.PaisModel import Pais
from app.models.TipoMovModel import TipoMovilidad

router = APIRouter(prefix="/utils", tags=["Utils"])

@router.get("/pais")
def listar_paises(db: Session = Depends(get_db)):
    paises = db.query(Pais.codigo_iso, Pais.nombre).all()
    data = [{"codigo_iso": p.codigo_iso, "nombre": p.nombre} for p in paises]
    return {"total": len(data), "data": data}


@router.get("/tipo_movilidad")
def listar_tipos_movilidades(db: Session = Depends(get_db)):
    tipo = db.query(TipoMovilidad).all()  
    return {"total": len(tipo), "data": tipo}
