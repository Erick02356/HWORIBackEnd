from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"  # nombre de la tabla
    __table_args__ = {'schema': 'parameters'}

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100))
    password = Column(String(255))
    
