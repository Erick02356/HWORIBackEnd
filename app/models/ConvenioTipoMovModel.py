from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class ConvenioTipoMovilidad(Base):
    __tablename__ = "convenio_tipo_movilidad"
    __table_args__ = {"schema": "operations"}

    convenio_codigo = Column(String(50), ForeignKey("operations.convenio.codigo"), primary_key=True)
    tipo_movilidad_codigo = Column(String(50), ForeignKey("operations.tipo_movilidad.codigo"), primary_key=True)
    
    convenio = relationship("Convenio", back_populates="tipos_movilidad")
    tipo_movilidad = relationship("TipoMovilidad", back_populates="convenios")  
