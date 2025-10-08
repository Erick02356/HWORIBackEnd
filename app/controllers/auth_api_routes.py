from fastapi import APIRouter, Form, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.UsuarioModel import Usuario
from app.utils.Bcrypt_password import verificarPassword
from app.utils.JWT import TokenManager

router = APIRouter()

# ---------------------------- LOGIN -------------------------------- #
@router.post("/auth/login")
def iniciar_sesion(
    response: Response,
    usuario: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Buscar usuario por nombre de usuario
        user = db.query(Usuario).filter(Usuario.usuario == usuario).first()

        if not user:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})

        # Verificar la contraseña con bcrypt
        if not verificarPassword(password, user.password):
            return JSONResponse(status_code=401, content={"message": "Credenciales incorrectas"})

        # Generar el token JWT
        token = TokenManager.generar_token(id=user.id, rol="user")

        res = JSONResponse(
            status_code=200,
            content={
                "message": "Inicio de sesión exitoso",
                "usuario": user.usuario,
                "token": token
            }
        )

        # Guardar token en cookie
        res.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=604800,  # 7 días
            path="/"
        )

        return res

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


# ---------------------------- LOGOUT -------------------------------- #
@router.post("/auth/logout")
def cerrar_sesion(response: Response):
    try:
        res = JSONResponse(status_code=200, content={"message": "Sesión cerrada exitosamente"})
        res.delete_cookie("access_token", path="/")
        return res
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
