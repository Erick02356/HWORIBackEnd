from fastapi import UploadFile, HTTPException
from pathlib import Path
from uuid import uuid4
import hashlib
from app.config.settings import settings

ALLOWED_EXT = {".xlsx", ".xls", ".csv"}

async def save_upload_to_disk(file: UploadFile) -> dict:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Formato no soportado ({suffix}).")

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    uid = uuid4().hex
    dest = upload_dir / f"{uid}{suffix}"

    size = 0
    hasher = hashlib.sha256()

    # Guardado por chunks para no saturar memoria y poder controlar tamaño
    with open(dest, "wb") as out:
        while True:
            chunk = await file.read(1024 * 1024)  # 1 MB
            if not chunk:
                break
            size += len(chunk)
            if size > settings.MAX_UPLOAD_MB * 1024 * 1024:
                out.close()
                dest.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail=f"El archivo excede {settings.MAX_UPLOAD_MB} MB.")
            hasher.update(chunk)
            out.write(chunk)

    await file.close()

    return {
        "id": uid,
        "file_path": str(dest),
        "file_name": file.filename,
        "ext": suffix,
        "size_bytes": size,
        "sha256": hasher.hexdigest(),
    }
