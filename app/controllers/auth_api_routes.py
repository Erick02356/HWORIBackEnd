# app/administrativo/routes/operativo_api_routes.py
import bcrypt
from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.models.UsuarioModel import Usuario
from app.services import JWT
from app.services.Bcrypt_password import verificarPassword
from app.services.JWT import TokenManager
from app.services.PostgresqlConexion import Postgresql
from fastapi import APIRouter, Request, Response, Form, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated
from typing import Annotated
import datetime
router = APIRouter()
#---------------------------- USUARIO API ENDPOINTS --------------------------------#
@router.post("/auth/login")
def iniciar_sesion(
    response: Response,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    try:
        usuario = Usuario.obtener_por_email(email)
        if usuario:
            response = usuario.iniciarSesion(password)
            if response:
                token = TokenManager.generar_token(id=usuario.id,rol=usuario.rol)
                res = JSONResponse(
                    status_code=200,
                    content={"message": "successful", "user": usuario.to_dict()}
                )
                # Agregamos el token como cookie segura
                res.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=True,       # Protege contra JS (XSS)
                    secure=False,         # Solo se envía por HTTPS
                    samesite="Lax",      # Protección CSRF (ajústalo si usas cross-site)
                    max_age=604800,        # Opcional: tiempo de expiración (en segundos)
                    path="/"
                )
                return res
        return JSONResponse(status_code=404, content={"message":"Credenciales Incorrectas"})

    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})
    

@router.post("/auth/logout")
def cerrar_sesion(response: Response):
    try:
        # Eliminar la cookie de acceso configurando su fecha de expiración en el pasado
        res= JSONResponse(status_code=200, content={"message": "Sesión cerrada exitosamente"})
        res.delete_cookie("access_token", path="/")
        
        # Responder que la sesión ha sido cerrada exitosamente
        return res

    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'message': str(e)})