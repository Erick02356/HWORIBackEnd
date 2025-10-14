from pathlib import Path
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Header, Depends
from app.config.settings import settings
from app.services.carga_service import save_upload_to_disk
from app.services.n8n_service import trigger_n8n_with_file
from app.config.security import get_current_user

router = APIRouter(prefix="/ingesta", tags=["Ingesta"])

@router.post("/upload-excel")
async def upload_excel(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    meta = await save_upload_to_disk(file)

    # Disparar n8n en background para no bloquear la respuesta
    metadata = {"ingestion_id": meta["id"], "sha256": meta["sha256"], "size_bytes": meta["size_bytes"]}
    background_tasks.add_task(
        trigger_n8n_with_file,
        Path(meta["file_path"]),
        meta["file_name"],
        metadata,
    )

    return {
        "message": "Archivo recibido, flujo n8n encolado.",
        "ingestion_id": meta["id"],
        "filename": meta["file_name"],
        "size_bytes": meta["size_bytes"],
        "status": "queued",
    }
