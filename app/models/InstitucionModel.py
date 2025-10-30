from sqlalchemy import Column, String
from app.config.database import Base

class Institucion(Base):
    __tablename__ = "institucion"  # nombre de la tabla
    __table_args__ = {'schema': 'operations'}

    codigo = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    direccion = Column(String(300))
    representante_legal = Column(String(150))
    correo = Column(String(150))
    telefono = Column(String(50))
    codigo_pais = Column(String(3))
    estado = Column(String(20), default="Activo")  