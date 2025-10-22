# app/controllers/auth_controller.py
from fastapi import APIRouter, Form, Response, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt

from app.config.database import get_db
from app.models.UsuarioModel import Usuario
from app.repositories.usuario_repository import (
    get_usuario, get_usuario_por_usuario, get_usuario_por_correo
)
from app.utils.Bcrypt_password import verificarPassword, generarPassword
from app.utils.JWT import TokenManager
from app.config.settings import settings
from app.services.email_service import send_email

# ------- utilidades para reset password -------
def _pwd_fp(pwd_hash: str) -> str:
    # huella simple del hash (invalida tokens antiguos si la clave cambió)
    return (pwd_hash or "")[:12]

def make_reset_token(user: Usuario) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "t": "pwdreset",
        "pwd_fp": _pwd_fp(user.password),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.PASSWORD_RESET_EXPIRES_MIN)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALG)

def verify_reset_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
    if payload.get("t") != "pwdreset":
        raise jwt.InvalidTokenError("Tipo de token inválido")
    return payload

# ------- esquemas pydantic -------
class ForgotPasswordIn(BaseModel):
    correo: EmailStr

class ResetPasswordIn(BaseModel):
    token: str = Field(..., min_length=10)
    password: str = Field(..., min_length=8)


router = APIRouter(prefix="/auth", tags=["Auth"])

# ---------------------------- LOGIN -------------------------------- #
@router.post("/login")
def iniciar_sesion(
    response: Response,
    usuario: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Buscar usuario por username
    user = get_usuario_por_usuario(db, usuario)
    if not user:
        return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})

    if user.estado != "Activo":
        return JSONResponse(status_code=403, content={"message": "Usuario inactivo"})

    # Verificar contraseña
    if not verificarPassword(password, user.password):
        return JSONResponse(status_code=401, content={"message": "Credenciales incorrectas"})

    # Generar el JWT de sesión (incluyendo el rol)
    # Si tu TokenManager ya añade 'rol' al payload, basta con pasar user.rol
    token = TokenManager.generar_token(id=user.id, rol=str(user.rol))

    res = JSONResponse(
        status_code=200,
        content={
            "message": "Inicio de sesión exitoso",
            "usuario": user.usuario,
            "token": token
        }
    )

    # Cookie (opcional si usas Authorization: Bearer en el front)
    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
        max_age=60 * 60 * 24 * 7,  # 7 días
        path="/"
    )

    return res


# ---------------------------- LOGOUT -------------------------------- #
@router.post("/logout")
def cerrar_sesion(response: Response):
    res = JSONResponse(status_code=200, content={"message": "Sesión cerrada exitosamente"})
    res.delete_cookie("access_token", path="/")
    return res


# ----------------------- FORGOT PASSWORD ---------------------------- #
@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(body: ForgotPasswordIn, db: Session = Depends(get_db)):
    """
    Devuelve 200 siempre. Si EMAIL_ENABLED=false, retorna token/reset_url para desarrollo.
    """
    user = get_usuario_por_correo(db, body.correo)
    # Nunca revelamos si el correo existe. Si existe y está activo, generamos token.
    if user and user.estado == "Activo":
        token = make_reset_token(user)
        reset_url = f"{settings.FRONTEND_RESET_URL}?token={token}"

        sent = send_email(
            to=body.correo,
            subject="Restablecer contraseña",
            html=f"""
                <p>Hola {user.nombre or user.usuario},</p>
                <p>Usa este enlace para restablecer tu contraseña (válido por tiempo limitado):</p>
                <p><a href="{reset_url}">{reset_url}</a></p>
                <p>Si no solicitaste este cambio, ignora este mensaje.</p>
            """
        )
        if sent:
            return {"message": "Si el correo existe, se ha enviado un enlace para restablecer la contraseña."}
        else:
            # Modo desarrollo / sin SMTP
            return {
                "message": "Modo desarrollo: token generado (sin correo).",
                "reset_token": token,
                "reset_url": reset_url
            }

    # Respuesta genérica (privacidad)
    return {"message": "Si el correo existe, se ha enviado un enlace para restablecer la contraseña."}


# ----------------------- RESET PASSWORD ----------------------------- #
@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(body: ResetPasswordIn, db: Session = Depends(get_db)):
    try:
        payload = verify_reset_token(body.token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="El enlace ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Token inválido")

    user_id = payload.get("sub")
    user = get_usuario(db, int(user_id))
    if not user or user.estado != "Activo":
        raise HTTPException(status_code=400, detail="Token inválido")

    # Token emitido antes de un cambio de clave previo → inválido
    if payload.get("pwd_fp") != _pwd_fp(user.password):
        raise HTTPException(status_code=400, detail="Token inválido o ya utilizado")

    # Actualizar contraseña
    user.password = generarPassword(body.password)
    db.commit()

    return {"message": "Contraseña actualizada correctamente"}


# ------------------------------ ME --------------------------------- #
@router.get("/me", status_code=status.HTTP_200_OK)
def me(request: Request, db: Session = Depends(get_db)):
    """
    Devuelve datos públicos del usuario autenticado.
    Lee el token de Authorization: Bearer o de la cookie 'access_token'.
    """
    token = None
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")

    # Decodificamos el token de sesión (mismo secreto/algoritmo que TokenManager)
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("sub") or payload.get("id") or payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = get_usuario(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"data": user.to_public_dict()}
