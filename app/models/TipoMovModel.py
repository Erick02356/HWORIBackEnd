from sqlalchemy import Column, Integer, String
from app.config.database import Base

class TipoMov(Base):
    __tablename__ = "tipo_movilidad"  # nombre de la tabla

    codigo = Column(String(50), primary_key=True)
    nombre = Column(String(150))
