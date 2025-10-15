from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Convenio(Base):
    __tablename__ = "convenio"
    __table_args__ = {"schema": "operations"}

    codigo = Column(String(50), primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    tipo = Column(String(100))
    fecha_inicio = Column(Date)
    fecha_finalizacion = Column(Date)
    estado = Column(String(20), default="Activo")
    codigo_institucion = Column(String(50), ForeignKey("operations.institucion.codigo"))

    # Relaciones
    institucion = relationship("Institucion", backref="convenios")
    tipos_movilidad = relationship(
        "ConvenioTipoMovilidad", back_populates="convenio", cascade="all, delete-orphan"
    )
