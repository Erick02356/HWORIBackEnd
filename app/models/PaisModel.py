from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Pais(Base):
    __tablename__ = "pais"  # nombre de la tabla
    __table_args__ = {'schema': 'operations'}

    codigo_iso = Column(String(3), primary_key=True)
    nombre = Column(String(150))
    codigo_iso2 = Column(String(2))
    codigo_iso3 = Column(String(3))
