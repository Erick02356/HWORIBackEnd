from fastapi import Cookie, HTTPException, Request,APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.utils.JWT import TokenManager

router = APIRouter()
templates = Jinja2Templates(directory="app/views")

#----------------------------------------------- PUBLICO --------------------------------------------------#

@router.get("/", response_class=HTMLResponse)
async def login(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("public/login.html", context)

@router.get("/registro", response_class=HTMLResponse)
async def registro(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("public/registro.html", context)


#------------------------------------- ADMIN -------------------------------------#
@router.get("/usuarios", response_class=HTMLResponse)
async def usuarios(request: Request,access_token: str = Cookie(None)):
    context = {
        "request": request,
        "es_htmx": "HX-Request" in request.headers
    }
    sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    if not sesion[0]:  return templates.TemplateResponse("dashboard/redirect-login.html", context)
    return templates.TemplateResponse("dashboard/administrador/usuarios.html", context)

@router.get("/programas_academicos", response_class=HTMLResponse)
async def programas_academicos(request: Request,access_token: str = Cookie(None)):
    context = {
        "request": request,
        "es_htmx": "HX-Request" in request.headers
    }
    sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    if not sesion[0]:  return templates.TemplateResponse("dashboard/redirect-login.html", context)
    return templates.TemplateResponse("dashboard/administrador/programas_academicos.html", context)

@router.get("/programas_movilidad", response_class=HTMLResponse)
async def programas_academicos(request: Request,access_token: str = Cookie(None)):
    context = {
        "request": request,
        "es_htmx": "HX-Request" in request.headers
    }
    sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    if not sesion[0]:  return templates.TemplateResponse("dashboard/redirect-login.html", context)
    return templates.TemplateResponse("dashboard/administrador/programas_movilidad.html", context)

#----------------------------------------------------------------------------------------------------------#

#------------------------------------- COORDINADOR MOVILIDAD SALIENTE -------------------------------------#
@router.get("/inicio", response_class=HTMLResponse)
async def dashboard(request: Request,access_token: str = Cookie(None)):
    context = {
        "request": request,
        "es_htmx": "HX-Request" in request.headers
    }
    sesion = TokenManager.validar_sesion_token(access_token,["est-out","coord-out","coord-inc","admin"])
    if not sesion[0]:  return templates.TemplateResponse("dashboard/redirect-login.html", context)
    return templates.TemplateResponse("dashboard/inicio.html", context)

@router.get("/convocatorias", response_class=HTMLResponse)
async def convocatorias(request: Request,access_token: str = Cookie(None)):
    context = {
        "request": request,
        "es_htmx": "HX-Request" in request.headers
    }
    sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    if not sesion[0]:  return templates.TemplateResponse("dashboard/redirect-login.html", context)
    return templates.TemplateResponse("dashboard/coordinador-saliente/convocatorias.html", context)

@router.get("/postulaciones", response_class=HTMLResponse)
async def postulaciones(request: Request,access_token: str = Cookie(None)):
    context = {
        "request": request,
        "es_htmx": "HX-Request" in request.headers
    }
    sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    if not sesion[0]:  return templates.TemplateResponse("dashboard/redirect-login.html", context)
    return templates.TemplateResponse("dashboard/coordinador-saliente/postulaciones.html", context)

@router.get("/movilidades", response_class=HTMLResponse)
async def movilidades(request: Request,access_token: str = Cookie(None)):
    context = {
        "request": request,
        "es_htmx": "HX-Request" in request.headers
    }
    sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    if not sesion[0]:  return templates.TemplateResponse("dashboard/redirect-login.html", context)
    return templates.TemplateResponse("dashboard/coordinador-saliente/movilidades.html", context)
#----------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------#
