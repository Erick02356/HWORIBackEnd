from app.repositories import institucion_repository

class InstitucionService:

    @staticmethod
    def listar(db, skip=0, limit=25):
        return institucion_repository.get_instituciones(db, skip, limit)

    @staticmethod
    def obtener_por_codigo(db, codigo: str):
        return institucion_repository.get_institucion(db, codigo)

    @staticmethod
    def crear(db, data: dict):
        return institucion_repository.crear_institucion(db, data)

    @staticmethod
    def actualizar(db, codigo: str, data: dict):
        return institucion_repository.actualizar_institucion(db, codigo, data)

    @staticmethod
    def eliminar(db, codigo: str):
        return institucion_repository.eliminar_institucion(db, codigo)
