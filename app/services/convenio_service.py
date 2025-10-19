from sqlalchemy.orm import Session
from app.repositories import convenio_repository


class ConvenioService:
    # Crear convenio con tipos de movilidad
    @staticmethod
    def crear(db: Session, convenio_data: dict):
        tipos_movilidad = convenio_data.pop("tipos_movilidad", [])
        return convenio_repository.crear_convenio(db, convenio_data, tipos_movilidad)

    # Obtener todos los convenios
    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 25):
        return convenio_repository.get_convenios(db, skip, limit)

    # Obtener los convenios con su institucion
    @staticmethod
    def listar_con_movilidades(db, skip=0, limit=25):
        return convenio_repository.get_convenios_with_movilidades(db, skip, limit)
    # Obtener convenio por código
    @staticmethod
    def obtener_por_codigo(db: Session, codigo: str):
        return convenio_repository.get_convenio_detalle(db, codigo)

    # Actualizar convenio
    @staticmethod
    def actualizar(db, codigo: str, body: dict):
        tipos = body.pop("tipos_movilidad", None)  # puede venir o no
        return convenio_repository.actualizar_convenio(db, codigo, body, tipos)
    
    # Eliminar convenio (lógica)
    @staticmethod
    def eliminar(db: Session, codigo: str):
        return convenio_repository.eliminar_convenio(db, codigo)
