from pathlib import Path
import httpx
from app.config.settings import settings

# Enviamos el archivo al Webhook de n8n junto con metadata
async def trigger_n8n_with_file(file_path: Path, original_name: str, metadata: dict) -> dict:
    headers = {}

    mime = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if file_path.suffix.lower() == ".xlsx"
        else "application/vnd.ms-excel"
    )

    data = {**metadata, "file_name": original_name}

    async with httpx.AsyncClient(timeout=120) as client:
        with open(file_path, "rb") as fh:
            files = {"file": (original_name, fh, mime)}
            resp = await client.post(settings.N8N_WEBHOOK_URL, data=data, files=files, headers=headers)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            return {"status_code": resp.status_code, "text": resp.text}
