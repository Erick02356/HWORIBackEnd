from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.utils.JWT import TokenManager

# Swagger usará este esquema para mostrar el candado 🔒 "Authorize"
bearer_scheme = HTTPBearer(auto_error=False)

# Dependencia para validar el token automáticamente
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no proporcionadas o inválidas",
        )

    token = credentials.credentials
    payload = TokenManager.validar_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    return payload  # ← payload contiene 'id' y 'rol'
