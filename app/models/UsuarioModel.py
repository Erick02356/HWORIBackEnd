from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"  # nombre de la tabla

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100))
    password = Column(String(255))
    
