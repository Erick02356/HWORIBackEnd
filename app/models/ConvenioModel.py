from sqlalchemy import Column, Integer, String, Date
from app.config.database import Base

class Convenio(Base):
    __tablename__ = "convenio"  # nombre de la tabla

    codigo = Column(Integer, primary_key=True)
    nombre = Column(String(200))
    tipo = Column(String(100))
    fecha_inicio = Column(Date)
    fecha_inicializacion = Column(Date)
    estado = Column(String(50))
    codigo_institucion = Column(String(50))
