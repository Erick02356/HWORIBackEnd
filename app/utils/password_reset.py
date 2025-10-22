from datetime import datetime, timedelta, timezone
import jwt
from app.config.settings import settings
from app.models.UsuarioModel import Usuario

def _fp(pwd_hash: str) -> str:
    return (pwd_hash or "")[:12]

def make_reset_token(user: Usuario) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "t": "pwdreset",
        "pwd_fp": _fp(user.password),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.PASSWORD_RESET_EXPIRES_MIN)).timestamp()),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALG)

def verify_reset_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALG])
