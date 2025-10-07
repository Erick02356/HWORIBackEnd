import jwt
import os
from datetime import datetime, timedelta

class TokenManager:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = 'HS256' # Algoritmo de firma

    @classmethod
    def generar_token(cls, id ,rol):
        ahora = datetime.now()
        expiracion = ahora + timedelta(days=7)
        payload = {
            'id': id,  
            'rol': rol,                # 'sub' se refiere al sujeto del token (el usuario)       
            'iat': int(ahora.timestamp()),                   # Fecha de emisión
            'exp': int(expiracion.timestamp())               # Fecha de expiración
        }
        
        token = jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def validar_token(cls, token:str):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload 
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
    @classmethod    
    def validar_sesion_token(cls, token:str, roles):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            if(payload["rol"] in roles):
                return [True,payload]
            else:
                return [False,"No tienes permisos"]
        except jwt.ExpiredSignatureError:
            return [False,"Token vencido"]
        except jwt.InvalidTokenError:
            return [False,"Token no valido"]
