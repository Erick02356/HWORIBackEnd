from typing import Literal
from pydantic import BaseModel

class NotificacionConvenio(BaseModel):
    id: str
    convenioCodigo: str
    titulo: str
    mensaje: str
    diasRestantes: int
    severidad: Literal['warn', 'danger']

    class Config:
        from_attributes = True  
