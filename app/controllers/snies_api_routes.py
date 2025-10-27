from fastapi import APIRouter, Query
from app.services.n8n_service import proxy_n8n_download_by_name

router = APIRouter(prefix="/snies", tags=["Snies"])

@router.get("/download")
async def download(name: str = Query(..., min_length=3, description="Texto completo, ej: 'Movilidad de estudiantes del exterior hacia Colombia 2025-1'")):
    # Devuelve StreamingResponse (archivo)
    return await proxy_n8n_download_by_name(name)