from sqlalchemy import Column, Integer, String
from app.config.database import Base

class ConvenioTipoMov(Base):
    __tablename__ = "convenio_tipo_movilidad"  # nombre de la tabla

    convenio_codigo = Column(String(50), primary_key=True)
    tipo_movilidad_codigo = Column(String(50), primary_key=True)
