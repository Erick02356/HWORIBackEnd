# app/models/UsuarioModel.py
from sqlalchemy import Column, Integer, String, Enum, DateTime, text
from app.config.database import Base
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

# Define enums en SQLAlchemy (utiliza los que ya existen en DB)
ROL_ENUM = PG_ENUM('admin', 'director', 'coordinador', name='rol_usuario_enum', schema='parameters', create_type=False)
ESTADO_ENUM = PG_ENUM('Activo', 'Inactivo', name='estado_usuario_enum', schema='parameters', create_type=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'schema': 'parameters'}

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    nombre = Column(String(150), nullable=True)
    correo = Column(String(255), unique=True, nullable=True, index=True)

    rol = Column(ROL_ENUM, nullable=False, server_default=text("'coordinador'::parameters.rol_usuario_enum"))
    estado = Column(ESTADO_ENUM, nullable=False, server_default=text("'Activo'::parameters.estado_usuario_enum"))

    ultimo_acceso = Column(DateTime(timezone=True), nullable=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))
    actualizado_en = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    def to_public_dict(self):
        # Nunca expongas el hash del password
        return {
            "id": self.id,
            "usuario": self.usuario,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol,
            "estado": self.estado,
            "ultimo_acceso": self.ultimo_acceso,
            "creado_en": self.creado_en,
            "actualizado_en": self.actualizado_en,
        }
