from sqlalchemy.orm import Session
from app.models.PaisModel import Pais

def get_paises(db: Session):
    return db.query(Pais).all()
