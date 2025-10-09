from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class TipoMovilidad(Base):
    __tablename__ = "tipo_movilidad"
    __table_args__ = {"schema": "operations"}

    codigo = Column(String(50), primary_key=True)
    nombre = Column(String(150))

    # Relación con la tabla intermedia
    convenios = relationship("ConvenioTipoMovilidad", back_populates="tipo_movilidad")
