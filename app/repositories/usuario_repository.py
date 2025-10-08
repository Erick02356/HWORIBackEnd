from sqlalchemy.orm import Session
from app.models.UsuarioModel import Usuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 25):
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def crear_usuario(db: Session, usuario: Usuario):
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, user_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False
