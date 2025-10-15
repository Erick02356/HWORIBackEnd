from sqlalchemy.orm import Session
from app.models.InstitucionModel import Institucion
from app.models.PaisModel import Pais


# Obtener todas las instituciones activas
def get_instituciones(db: Session, skip: int = 0, limit: int = 25):
    return (
        db.query(
            Institucion.codigo,
            Institucion.nombre,
            Institucion.direccion,
            Institucion.representante_legal,
            Institucion.correo,
            Institucion.telefono,
            Institucion.estado,
            Institucion.codigo_pais,
            Pais.nombre.label("nombre_pais")
        )
        .join(Pais, Institucion.codigo_pais == Pais.codigo_iso)
        .filter(Institucion.estado == "Activo")
        .offset(skip)
        .limit(limit)
        .all()
    )

# Obtener una institucion activa
def get_institucion(db: Session, codigo: str):
    return (
        db.query(
            Institucion.codigo,
            Institucion.nombre,
            Institucion.direccion,
            Institucion.representante_legal,
            Institucion.correo,
            Institucion.telefono,
            Institucion.estado,
            Institucion.codigo_pais,
            Pais.nombre.label("nombre_pais")
        )
        .join(Pais, Institucion.codigo_pais == Pais.codigo_iso)
        .filter(Institucion.codigo == codigo, Institucion.estado == "Activo")
        .first()
    )
# Crear una institución
def crear_institucion(db: Session, institucion_data: dict):
    nueva_institucion = Institucion(**institucion_data)
    db.add(nueva_institucion)
    db.commit()
    db.refresh(nueva_institucion)
    return nueva_institucion

# Actualizar una institución
def actualizar_institucion(db: Session, codigo: str, updates: dict):
    institucion = db.query(Institucion).filter(Institucion.codigo == codigo).first()
    if not institucion or institucion.estado != "Activo":
        return None
    for key, value in updates.items():
        setattr(institucion, key, value)
    db.commit()
    db.refresh(institucion)
    return institucion

# Eliminación lógica (cambia estado a 'Inactivo')
def eliminar_institucion(db: Session, codigo: str):
    institucion = db.query(Institucion).filter(Institucion.codigo == codigo).first()
    if institucion and institucion.estado != "Inactivo":
        institucion.estado = "Inactivo"
        db.commit()
        db.refresh(institucion)
        return True
    return False
