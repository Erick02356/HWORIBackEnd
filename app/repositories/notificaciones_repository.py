from typing import List, Tuple
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.models.ConvenioModel import Convenio  

def fetch_convenios_por_vencer(
    db: Session,
    *,
    max_days: int = 90,
    min_days: int = 1,
    solo_activos: bool = True,
    limit: int = 100,
    offset: int = 0,
) -> List[Tuple[Convenio, int]]:
    """
    Retorna (Convenio, dias_restantes) para convenios con fecha_finalizacion en 1..max_days días.
    Usa CURRENT_DATE sin paréntesis para evitar el warning de Pylint.
    """
    current_date = sa.literal_column("CURRENT_DATE")  # <- evita Pylint E1102

    # Si fecha_finalizacion ya es DATE, no hace falta cast. Si es TIMESTAMP, descomenta el cast:
    # end_date = sa.cast(Convenio.fecha_finalizacion, sa.Date)
    end_date = Convenio.fecha_finalizacion

    diff_days_expr = (end_date - current_date)
    dias_restantes_expr = sa.func.greatest(diff_days_expr, 0).label("dias_restantes")

    conditions = [
        end_date.isnot(None),
        diff_days_expr >= min_days,
        diff_days_expr <= max_days,
    ]
    if solo_activos:
        conditions.append(sa.func.lower(Convenio.estado) == "activo")

    q = (
        db.query(Convenio, dias_restantes_expr)
        .filter(sa.and_(*conditions))
        .order_by(Convenio.fecha_finalizacion.asc())
        .offset(offset)
        .limit(limit)
    )

    return [(row[0], int(row[1])) for row in q.all()]
