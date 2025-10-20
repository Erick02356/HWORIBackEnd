# app/repositories/usuario_repository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.UsuarioModel import Usuario
from app.utils.Bcrypt_password import generarPassword

def get_usuarios(db: Session, skip: int = 0, limit: int = 25):
    q = db.query(Usuario).order_by(Usuario.id.desc())
    items = q.offset(skip).limit(limit).all()
    total = db.query(Usuario).count()
    return items, total

def get_usuario(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_usuario_por_usuario(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_usuario_por_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()

def crear_usuario(db: Session, data: dict) -> Usuario:
    # data: {usuario, password, nombre?, correo?, rol?, estado?}
    entity = Usuario(
        usuario=data["usuario"],
        password=generarPassword(data["password"]),
        nombre=data.get("nombre"),
        correo=data.get("correo"),
        rol=data.get("rol", "coordinador"),
        estado=data.get("estado", "Activo"),
    )
    db.add(entity)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Unicidad usuario/correo
        raise ValueError("Usuario o correo ya existen") from e
    db.refresh(entity)
    return entity

def actualizar_usuario(db: Session, user_id: int, updates: dict) -> Usuario | None:
    u = get_usuario(db, user_id)
    if not u:
        return None

    allowed = {"usuario", "nombre", "correo", "rol", "estado", "password"}
    for k, v in updates.items():
        if k not in allowed:
            continue
        if k == "password":
            if v:
                setattr(u, "password", generarPassword(v))
        else:
            setattr(u, k, v)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Usuario o correo ya existen") from e

    db.refresh(u)
    return u

def desactivar_usuario(db: Session, user_id: int) -> bool:
    u = get_usuario(db, user_id)
    if not u:
        return False
    u.estado = "Inactivo"
    db.commit()
    return True

# Opcional: borrado físico (no recomendado en producción)
def eliminar_usuario(db: Session, user_id: int) -> bool:
    u = get_usuario(db, user_id)
    if not u:
        return False
    db.delete(u)
    db.commit()
    return True
