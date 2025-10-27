from pathlib import Path
import re, unicodedata, urllib.parse
import httpx
from fastapi import HTTPException, Response
from fastapi.responses import StreamingResponse
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
        


async def proxy_n8n_download_by_name(name: str) -> Response:
    if not getattr(settings, "N8N_DOWNLOAD_WEBHOOK_URL", None):
        raise HTTPException(500, "N8N_DOWNLOAD_WEBHOOK_URL no configurado")

    headers = {}
    api_key = getattr(settings, "N8N_API_KEY", None)
    if api_key:
        headers["x-api-key"] = api_key

    params = {"name": name}

    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        r = await client.get(settings.N8N_DOWNLOAD_WEBHOOK_URL, params=params, headers=headers)

    if r.status_code == 404:
        raise HTTPException(404, "Archivo no encontrado")
    r.raise_for_status()

    content_type = r.headers.get(
        "content-type",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    disposition = r.headers.get("content-disposition")
    if not disposition:
        disposition = f'attachment; filename="{_safe_filename(name)}"'

    # LEE el contenido completo ANTES de devolver la respuesta
    data = r.content

    # Desactiva caché del navegador (y de Swagger UI)
    no_cache = {
        "Content-Disposition": disposition,
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }
    return Response(content=data, media_type=content_type, headers=no_cache)


def _safe_filename(raw: str) -> str:
    s = unicodedata.normalize("NFKD", raw).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w.\- ]+", "_", s).strip()
    if not s.lower().endswith(".xlsx"):
        s += ".xlsx"
    return urllib.parse.quote(s)