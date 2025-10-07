# app/administrativo/routes/operativo_api_routes.py
import bcrypt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from app.models.UsuarioModel import Usuario
from app.services import JWT
from app.services.Bcrypt_password import verificarPassword
from app.services.JWT import TokenManager
from app.services.PostgresqlConexion import Postgresql
from fastapi import APIRouter, Request, Response, Form, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from typing import Annotated
import datetime
router = APIRouter()
#---------------------------- USUARIO API ENDPOINTS --------------------------------#
@router.get("/usuario")
async def getUsuarios(access_token: str = Cookie(None),
                    cantidad: int = Query(25, description="Cantidad de usuarios por página", ge=1, le=100),
                    pagina: int = Query(1, description="Número de página", ge=1)):
    sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    if not sesion[0]:  return JSONResponse(status_code=401, content={"message": sesion[1]})
    if cantidad not in [10,25,50,100]:
        return JSONResponse(status_code=400, content={"message": f"cantidad debe ser uno de 10, 25, 50 o 100"})
    try:
        usuarios = Usuario.obtener_todos(cantidad=cantidad,pagina=pagina)
        if usuarios:
            return JSONResponse(status_code=200, content={"registrados":usuarios[0],"pagina":pagina,"usuarios": usuarios[1]})
        else:
            return JSONResponse(status_code=200, content={"registrados":usuarios[0],"pagina":pagina,"usuarios":[]})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})

@router.get("/usuario/{id}")
async def getUsuario(id: int):
    try:
        usuario = Usuario.obtener_por_id(id)
        if usuario:
            return JSONResponse(status_code=200, content={"usuario": usuario.to_dict()})
        else:
            return JSONResponse(status_code=404, content={"message":"Usuario no encontrado"})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})

@router.post("/usuario")
def createUsuario(
        nombres: Annotated[str, Form()],
        apellidos: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        rol: Annotated[str, Form()],):
    try:
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            password=password,
            rol=rol
        )
        result = Usuario.create(nuevo_usuario)
        if result[0]: 
            return JSONResponse(status_code=201, content={"message":"creado con exito"}
        )
        else:
            return JSONResponse(status_code=409, content={'message': result[1]}
        )
            
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})

@router.delete("/usuario/{id}")
async def deleteUsuario(id: int):
    try:
            #sesion = TokenManager.validar_sesion_token(access_token,["admin"])
    #if not sesion[0]:  return JSONResponse(status_code=401, content={"message": sesion[1]})
        usuario = Usuario.obtener_por_id(id)
        if usuario:
            if usuario.delete():
                return JSONResponse(status_code=200, content={"message": "eliminado con exito"})
            else:
                return JSONResponse(status_code=200, content={"message": "error al eliminar"})
        else:
            return JSONResponse(status_code=404, content={"message":"Usuario no encontrado"})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': str(e)})