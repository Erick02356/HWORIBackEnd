from sqlalchemy.orm import Session
from sqlalchemy import text

class DashboardRepository:

    @staticmethod
    def listar_movilidades(db: Session):
        sql = text("""
            SELECT "año" AS anio, semestre, total_movilidades
            FROM datawarehouse.mv_movilidades_por_tiempo
            ORDER BY "año", semestre
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_pais(db: Session):
        sql = text("""
            SELECT paisorigen, paisdestino, total_movilidades
            FROM datawarehouse.mv_movilidades_por_pais
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_programa(db: Session):
        sql = text("""
            SELECT nombreprograma, facultad, total_movilidades
            FROM datawarehouse.mv_movilidades_por_programa
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_convenio(db: Session):
        sql = text("""
            SELECT codigoconvenio, total_movilidades
            FROM datawarehouse.mv_movilidades_por_convenio
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_institucion(db: Session):
        sql = text("""
            SELECT institucionorigen, instituciondestino, total_movilidades
            FROM datawarehouse.mv_movilidades_por_institucion
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_genero(db: Session):
        sql = text("""
            SELECT genero, total_movilidades
            FROM datawarehouse.mv_movilidades_por_genero
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_direccion(db: Session):
        sql = text("""
            SELECT direccion, total_movilidades
            FROM datawarehouse.mv_movilidades_por_direccion
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_tipo(db: Session):
        sql = text("""
            SELECT tipo, total_movilidades
            FROM datawarehouse.mv_movilidades_por_tipo
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def listar_por_modalidad(db: Session):
        sql = text("""
            SELECT modalidad, total_movilidades
            FROM datawarehouse.mv_movilidades_por_modalidad
            ORDER BY total_movilidades DESC
        """)
        return db.execute(sql).fetchall()

    # ---- TOP/BOTTOM views ----
    @staticmethod
    def semestre_top(db: Session):
        sql = text("""
            SELECT "año", semestre, total_movilidades
            FROM datawarehouse.mv_movilidades_por_tiempo
            ORDER BY total_movilidades DESC
            LIMIT 1
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def paises_top10(db: Session):
        sql = text("""
            SELECT paisorigen, paisdestino, total_movilidades
            FROM datawarehouse.mv_movilidades_por_pais
            ORDER BY total_movilidades DESC
            LIMIT 10
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def paises_bottom10(db: Session):
        sql = text("""
            SELECT paisorigen, paisdestino, total_movilidades
            FROM datawarehouse.mv_movilidades_por_pais
            WHERE total_movilidades > 0
            ORDER BY total_movilidades ASC
            LIMIT 10
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def programa_top(db: Session):
        sql = text("""
            SELECT nombreprograma, total_movilidades
            FROM datawarehouse.mv_movilidades_por_programa
            ORDER BY total_movilidades DESC
            LIMIT 1
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def tipo_top(db: Session):
        sql = text("""
            SELECT tipo, total_movilidades
            FROM datawarehouse.mv_movilidades_por_tipo
            ORDER BY total_movilidades DESC
            LIMIT 1
        """)
        return db.execute(sql).fetchall()

    @staticmethod
    def convenio_top(db: Session):
        sql = text("""
            SELECT codigoconvenio, total_movilidades
            FROM datawarehouse.mv_movilidades_por_convenio
            ORDER BY total_movilidades DESC
            LIMIT 1
        """)
        return db.execute(sql).fetchall()

    # ---- FUNCIONES (periodo / top pais) ----
    @staticmethod
    def total_periodo(db: Session, anio: int, semestre: int):
        sql = text("""
            SELECT datawarehouse.fn_total_movilidades_periodo(:anio, :semestre)
        """)
        # scalar() devuelve valor único
        return db.execute(sql, {"anio": anio, "semestre": semestre}).scalar()

    @staticmethod
    def entrantes_periodo(db: Session, anio: int, semestre: int):
        sql = text("""
            SELECT datawarehouse.fn_movilidades_entrantes_periodo(:anio, :semestre)
        """)
        return db.execute(sql, {"anio": anio, "semestre": semestre}).scalar()

    @staticmethod
    def salientes_periodo(db: Session, anio: int, semestre: int):
        sql = text("""
            SELECT datawarehouse.fn_movilidades_salientes_periodo(:anio, :semestre)
        """)
        return db.execute(sql, {"anio": anio, "semestre": semestre}).scalar()

    @staticmethod
    def top_pais_periodo(db: Session, anio: int, semestre: int):
        sql = text("""
            SELECT paisorigen, total_movilidades FROM datawarehouse.fn_top_pais_origen_periodo(:anio, :semestre)
        """)
        return db.execute(sql, {"anio": anio, "semestre": semestre}).fetchall()
