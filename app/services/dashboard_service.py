from sqlalchemy.orm import Session
from app.repositories.dashboard_repository import DashboardRepository

class DashboardService:

    @staticmethod
    def listar_movilidades(db: Session):
        return DashboardRepository.listar_movilidades(db)

    @staticmethod
    def listar_por_pais(db: Session):
        return DashboardRepository.listar_por_pais(db)

    @staticmethod
    def listar_por_programa(db: Session):
        return DashboardRepository.listar_por_programa(db)

    @staticmethod
    def listar_por_convenio(db: Session):
        return DashboardRepository.listar_por_convenio(db)

    @staticmethod
    def listar_por_institucion(db: Session):
        return DashboardRepository.listar_por_institucion(db)

    @staticmethod
    def listar_por_genero(db: Session):
        return DashboardRepository.listar_por_genero(db)

    @staticmethod
    def listar_por_direccion(db: Session):
        return DashboardRepository.listar_por_direccion(db)

    @staticmethod
    def listar_por_tipo(db: Session):
        return DashboardRepository.listar_por_tipo(db)

    @staticmethod
    def listar_por_modalidad(db: Session):
        return DashboardRepository.listar_por_modalidad(db)

    # TOP / BOTTOM
    @staticmethod
    def semestre_top(db: Session):
        return DashboardRepository.semestre_top(db)

    @staticmethod
    def paises_top10(db: Session):
        return DashboardRepository.paises_top10(db)

    @staticmethod
    def paises_bottom10(db: Session):
        return DashboardRepository.paises_bottom10(db)

    @staticmethod
    def programa_top(db: Session):
        return DashboardRepository.programa_top(db)

    @staticmethod
    def tipo_top(db: Session):
        return DashboardRepository.tipo_top(db)

    @staticmethod
    def convenio_top(db: Session):
        return DashboardRepository.convenio_top(db)

    # Funciones
    @staticmethod
    def total_periodo(db: Session, anio: int, semestre: int):
        return DashboardRepository.total_periodo(db, anio, semestre)

    @staticmethod
    def entrantes_periodo(db: Session, anio: int, semestre: int):
        return DashboardRepository.entrantes_periodo(db, anio, semestre)

    @staticmethod
    def salientes_periodo(db: Session, anio: int, semestre: int):
        return DashboardRepository.salientes_periodo(db, anio, semestre)

    @staticmethod
    def top_pais_periodo(db: Session, anio: int, semestre: int):
        return DashboardRepository.top_pais_periodo(db, anio, semestre)
