from typing import List
from app.models.notificaciones_schema import NotificacionConvenio
from app.repositories.notificaciones_repository import fetch_convenios_por_vencer
from sqlalchemy.orm import Session

def construir_notifs_convenio(
    db: Session,
    *,
    max_days: int = 90,
    min_days: int = 1,
    solo_activos: bool = True,
    limit: int = 100,
    offset: int = 0,
) -> List[NotificacionConvenio]:
    """
    Construye las notificaciones para convenios por vencer en 1..max_days días.
    Regla de severidad: <=15 días -> 'danger', otro caso -> 'warn'.
    """
    filas = fetch_convenios_por_vencer(
        db,
        max_days=max_days,
        min_days=min_days,
        solo_activos=solo_activos,
        limit=limit,
        offset=offset,
    )

    notifs: List[NotificacionConvenio] = []
    for convenio, dias in filas:
        severidad = "danger" if dias <= 15 else "warn"
        notifs.append(
            NotificacionConvenio(
                id=f"conv-{convenio.codigo}",
                convenioCodigo=convenio.codigo,
                titulo="Convenio por vencer",
                mensaje=f'Faltan {dias} día{"s" if dias != 1 else ""} para que el convenio "{convenio.nombre}" venza.',
                diasRestantes=dias,
                severidad=severidad,
            )
        )

    # Ya vienen ordenadas por fecha_finalizacion asc; por si acaso, reordenamos por urgencia:
    notifs.sort(key=lambda n: n.diasRestantes)
    return notifs
