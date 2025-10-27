from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.security import get_current_user
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def _row_to_dict(row, fields):
    """
    row: SQLAlchemy row (tuple-like or object)
    fields: list of (target_key, idx_or_attrname)
    """
    result = {}
    for key, src in fields:
        try:
            if isinstance(src, int):
                result[key] = row[src]
            else:
                result[key] = getattr(row, src) if hasattr(row, src) else row[src]
        except Exception:
            result[key] = None
    return result

@router.get("/movilidades", status_code=status.HTTP_200_OK)
def listar_movilidades(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        movilidades = DashboardService.listar_movilidades(db)
        data = [
            {
                "anio": row.anio if hasattr(row, 'anio') else row[0],
                "semestre": row.semestre if hasattr(row, 'semestre') else row[1],
                "total_movilidades": row.total_movilidades if hasattr(row, 'total_movilidades') else row[2]
            }
            for row in movilidades
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Generic pattern endpoints (pais, programa, convenio, etc.)
@router.get("/paises", status_code=status.HTTP_200_OK)
def listar_por_pais(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_pais(db)
        data = [
            {"paisorigen": r.paisorigen if hasattr(r,'paisorigen') else r[0],
             "paisdestino": r.paisdestino if hasattr(r,'paisdestino') else r[1],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[2]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/programas", status_code=status.HTTP_200_OK)
def listar_por_programa(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_programa(db)
        data = [
            {"nombreprograma": r.nombreprograma if hasattr(r,'nombreprograma') else r[0],
             "facultad": r.facultad if hasattr(r,'facultad') else r[1],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[2]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/convenios", status_code=status.HTTP_200_OK)
def listar_por_convenio(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_convenio(db)
        data = [
            {"codigo": r.codigo if hasattr(r,'codigo') else r[0],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[1]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/instituciones", status_code=status.HTTP_200_OK)
def listar_por_institucion(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_institucion(db)
        data = [
            {"institucionorigen": r.institucionorigen if hasattr(r,'institucionorigen') else r[0],
             "instituciondestino": r.instituciondestino if hasattr(r,'instituciondestino') else r[1],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[2]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/generos", status_code=status.HTTP_200_OK)
def listar_por_genero(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_genero(db)
        data = [
            {"genero": r.genero if hasattr(r,'genero') else r[0],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[1]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/direcciones", status_code=status.HTTP_200_OK)
def listar_por_direccion(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_direccion(db)
        data = [
            {"direccion": r.direccion if hasattr(r,'direccion') else r[0],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[1]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tipos", status_code=status.HTTP_200_OK)
def listar_por_tipo(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_tipo(db)
        data = [
            {"tipo": r.tipo if hasattr(r,'tipo') else r[0],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[1]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/modalidades", status_code=status.HTTP_200_OK)
def listar_por_modalidad(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.listar_por_modalidad(db)
        data = [
            {"modalidad": r.modalidad if hasattr(r,'modalidad') else r[0],
             "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[1]}
            for r in rows
        ]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---- TOP / BOTTOM views ----
@router.get("/top/semestre", status_code=status.HTTP_200_OK)
def semestre_top(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        r = DashboardService.semestre_top(db)
        if not r:
            return {"total": 0, "usuario": current_user["id"], "data": []}
        row = r[0]
        data = {"anio": getattr(row,"año", None) or getattr(row,"anio", None) or row[0],
                "semestre": getattr(row,"semestre", None) or row[1],
                "total_movilidades": getattr(row,"total_movilidades", None) or row[2]}
        return {"total": 1, "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/top/paises", status_code=status.HTTP_200_OK)
def paises_top10(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.paises_top10(db)
        data = [{"paisorigen": r[0], "paisdestino": r[1], "total_movilidades": r[2]} for r in rows]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bottom/paises", status_code=status.HTTP_200_OK)
def paises_bottom10(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.paises_bottom10(db)
        data = [{"paisorigen": r[0], "paisdestino": r[1], "total_movilidades": r[2]} for r in rows]
        return {"total": len(data), "usuario": current_user["id"], "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/top/programa", status_code=status.HTTP_200_OK)
def programa_top(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        r = DashboardService.programa_top(db)
        if not r: return {"total": 0, "usuario": current_user["id"], "data": []}
        row = r[0]
        return {"total": 1, "usuario": current_user["id"], 
                "data": {"nombreprograma": row[0], "total_movilidades": row[1]}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/top/tipo", status_code=status.HTTP_200_OK)
def tipo_top(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        r = DashboardService.tipo_top(db)
        if not r: return {"total": 0, "usuario": current_user["id"], "data": []}
        row = r[0]
        return {"total": 1, "usuario": current_user["id"], "data": {"tipo": row[0], "total_movilidades": row[1]}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/top/convenio", status_code=status.HTTP_200_OK)
def convenio_top(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        r = DashboardService.convenio_top(db)
        if not r:
            return {"total": 0, "usuario": current_user["id"], "data": []}

        row = r[0]

        return {
            "total": 1,
            "usuario": current_user["id"],
            "data": {
                "codigo": row.codigo if hasattr(row, 'codigo') else row[0],
                "total_movilidades": row.total_movilidades if hasattr(row, 'total_movilidades') else row[1]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---- Funciones con parámetros (query params) ----
@router.get("/periodo/total", status_code=status.HTTP_200_OK)
def total_periodo(anio: int = Query(...), semestre: int = Query(...),
                  db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        total = DashboardService.total_periodo(db, anio, semestre)
        return {"anio": anio, "semestre": semestre, "total_movilidades": total}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/periodo/entrantes", status_code=status.HTTP_200_OK)
def entrantes_periodo(anio: int = Query(...), semestre: int = Query(...),
                      db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        total = DashboardService.entrantes_periodo(db, anio, semestre)
        return {"anio": anio, "semestre": semestre, "total_entrantes": total}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/periodo/salientes", status_code=status.HTTP_200_OK)
def salientes_periodo(anio: int = Query(...), semestre: int = Query(...),
                      db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        total = DashboardService.salientes_periodo(db, anio, semestre)
        return {"anio": anio, "semestre": semestre, "total_salientes": total}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/periodo/top_pais", status_code=status.HTTP_200_OK)
def top_pais_periodo(anio: int = Query(...), semestre: int = Query(...),
                     db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        rows = DashboardService.top_pais_periodo(db, anio, semestre)
        if not rows:
            return {"anio": anio, "semestre": semestre, "data": []}
        r = rows[0]
        return {"anio": anio, "semestre": semestre, "data": {"paisorigen": r.paisorigen if hasattr(r,'paisorigen') else r[0], "total_movilidades": r.total_movilidades if hasattr(r,'total_movilidades') else r[1]}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
