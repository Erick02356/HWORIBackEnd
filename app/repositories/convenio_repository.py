from sqlalchemy.orm import Session
from app.models import Convenio, ConvenioTipoMovilidad, TipoMovilidad, Institucion
from sqlalchemy import func
from datetime import date
from typing import Optional, List

# Crear un convenio con varios tipos de movilidad asociados
def crear_convenio(db: Session, convenio_data: dict, tipos_movilidad_codigos: list[str]):
    convenio = Convenio(**convenio_data)

    for codigo_tipo in tipos_movilidad_codigos:
        asociacion = ConvenioTipoMovilidad(
            convenio_codigo=convenio.codigo,
            tipo_movilidad_codigo=codigo_tipo  
        )
        db.add(asociacion)

    db.add(convenio)
    db.commit()
    db.refresh(convenio)
    return convenio


# Obtener todos los convenios activos
def get_convenios(db: Session, skip: int = 0, limit: int = 25):
    return (
        db.query(Convenio)
        .filter(Convenio.estado == "Activo")
        .offset(skip)
        .limit(limit)
        .all()
    )

#Obtener convenios tal y como lo pide el frontend
def get_convenios_with_movilidades(db: Session, skip: int = 0, limit: int = 25):
    query = (
        db.query(
            Convenio.codigo,
            Convenio.nombre.label("nombre_convenio"),
            Convenio.tipo,
            Convenio.fecha_inicio,
            Convenio.fecha_finalizacion,
            Convenio.estado,
            Institucion.nombre.label("nombre_institucion"),
            func.array_agg(TipoMovilidad.nombre).label("movilidades_convenio")
        )
        .join(Institucion, Convenio.codigo_institucion == Institucion.codigo)
        .join(ConvenioTipoMovilidad, ConvenioTipoMovilidad.convenio_codigo == Convenio.codigo)
        .join(TipoMovilidad, TipoMovilidad.codigo == ConvenioTipoMovilidad.tipo_movilidad_codigo)
        .filter(Convenio.estado != "inactivo")
        .group_by(
            Convenio.codigo,
            Convenio.nombre,
            Convenio.tipo,
            Convenio.fecha_inicio,
            Convenio.fecha_finalizacion,
            Convenio.estado,
            Institucion.nombre
        )
        .offset(skip)
        .limit(limit)
    )
    return query.all()

# Obtener convenio por código
def get_convenio_detalle(db: Session, codigo: str):
    row = (
        db.query(
            Convenio.codigo,
            Convenio.nombre,
            Convenio.tipo,
            Convenio.fecha_inicio,
            Convenio.fecha_finalizacion,
            Convenio.estado,
            Convenio.codigo_institucion,
            func.array_remove(
                func.array_agg(ConvenioTipoMovilidad.tipo_movilidad_codigo), None
            ).label("tipos_movilidad")
        )
        .outerjoin(ConvenioTipoMovilidad, Convenio.codigo == ConvenioTipoMovilidad.convenio_codigo)
        .filter(Convenio.codigo == codigo)
        .group_by(
            Convenio.codigo, Convenio.nombre, Convenio.tipo,
            Convenio.fecha_inicio, Convenio.fecha_finalizacion,
            Convenio.estado, Convenio.codigo_institucion
        )
        .first()
    )
    return row


# Actualizar un convenio
def _as_date(val):
    if val is None or isinstance(val, date):
        return val
    return date.fromisoformat(str(val))

def actualizar_convenio(db, codigo: str, updates: dict, tipos_movilidad_codigos: Optional[List[str]] = None):
    convenio = db.query(Convenio).filter(Convenio.codigo == codigo).first()
    if not convenio:
        return None

    # --- normaliza/valida campos simples ---
    allowed = {"nombre", "tipo", "fecha_inicio", "fecha_finalizacion", "estado", "codigo_institucion"}

    if "estado" in updates and updates["estado"] is not None:
        updates["estado"] = str(updates["estado"]).lower()

    if "fecha_inicio" in updates:
        updates["fecha_inicio"] = _as_date(updates["fecha_inicio"])
    if "fecha_finalizacion" in updates:
        updates["fecha_finalizacion"] = _as_date(updates["fecha_finalizacion"])

    if "codigo_institucion" in updates:
        inst = db.query(Institucion).filter(Institucion.codigo == updates["codigo_institucion"]).first()
        if not inst:
            raise ValueError(f"codigo_institucion '{updates['codigo_institucion']}' no existe")

    for k, v in updates.items():
        if k in allowed:
            setattr(convenio, k, v)

    # --- actualización DIFERENCIAL de la M:N ---
    if tipos_movilidad_codigos is not None:
        new_set = set(tipos_movilidad_codigos)

        # valida que los códigos existan
        existentes = {
            r[0] for r in db.query(TipoMovilidad.codigo)
                            .filter(TipoMovilidad.codigo.in_(new_set)).all()
        }
        faltantes = new_set - existentes
        if faltantes:
            raise ValueError(f"Tipos de movilidad inválidos: {sorted(faltantes)}")

        # set actual en DB
        current_rows = db.query(ConvenioTipoMovilidad)\
                         .filter(ConvenioTipoMovilidad.convenio_codigo == codigo).all()
        current_set = {r.tipo_movilidad_codigo for r in current_rows}

        to_add = new_set - current_set
        to_remove = current_set - new_set

        if to_remove:
            db.query(ConvenioTipoMovilidad).filter(
                ConvenioTipoMovilidad.convenio_codigo == codigo,
                ConvenioTipoMovilidad.tipo_movilidad_codigo.in_(to_remove)
            ).delete(synchronize_session=False)

        for cod in to_add:
            db.add(ConvenioTipoMovilidad(
                convenio_codigo=codigo,
                tipo_movilidad_codigo=cod
            ))

    db.commit()
    db.refresh(convenio)
    return convenio

# Eliminación lógica
def eliminar_convenio(db: Session, codigo: str):
    convenio = db.query(Convenio).filter(Convenio.codigo == codigo).first()
    if convenio and convenio.estado != "inactivo":
        convenio.estado = "inactivo"
        db.commit()
        db.refresh(convenio)
        return True
    return False
