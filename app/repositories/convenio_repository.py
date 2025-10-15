from sqlalchemy.orm import Session
from app.models import Convenio, ConvenioTipoMovilidad, TipoMovilidad, Institucion
from sqlalchemy import func


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
        .filter(Convenio.estado == "Activo")
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
def get_convenio(db: Session, codigo: str):
    return (
        db.query(Convenio)
        .filter(Convenio.codigo == codigo, Convenio.estado == "Activo")
        .first()
    )


# Actualizar un convenio
def actualizar_convenio(db: Session, codigo: str, updates: dict):
    convenio = db.query(Convenio).filter(Convenio.codigo == codigo).first()
    if not convenio:
        return None

    for key, value in updates.items():
        setattr(convenio, key, value)

    db.commit()
    db.refresh(convenio)
    return convenio


# Eliminación lógica
def eliminar_convenio(db: Session, codigo: str):
    convenio = db.query(Convenio).filter(Convenio.codigo == codigo).first()
    if convenio and convenio.estado != "Inactivo":
        convenio.estado = "Inactivo"
        db.commit()
        db.refresh(convenio)
        return True
    return False
