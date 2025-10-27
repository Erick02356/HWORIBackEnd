from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.notificaciones_schema import NotificacionConvenio
from app.services.notificaciones_service import construir_notifs_convenio

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

@router.get(
    "/convenios/proximos-vencer",
    response_model=List[NotificacionConvenio],
    summary="Lista notificaciones de convenios por vencer"
)
def listar_notificaciones_convenios_por_vencer(
    db: Session = Depends(get_db),
    max_days: int = Query(90, ge=1, le=3650, description="Umbral máximo de días (incluido)"),
    min_days: int = Query(1, ge=0, le=3650, description="Umbral mínimo de días (incluido)"),
    solo_activos: bool = Query(True, description="Si True, solo estado=Activo"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    Devuelve notificaciones para convenios cuya fecha_finalizacion está entre [min_days, max_days] días desde hoy.
    - Cálculo basado en CURRENT_DATE (sin TZ).
    - Por defecto incluye solo convenios 'Activo'.
    - Severidad: <=15 días => danger, otro caso => warn.
    """
    return construir_notifs_convenio(
        db,
        max_days=max_days,
        min_days=min_days,
        solo_activos=solo_activos,
        limit=limit,
        offset=offset,
    )
