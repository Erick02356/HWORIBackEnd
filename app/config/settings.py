# app/config/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ------------------------
    # Configuración general
    # ------------------------
    DEBUG: bool = True

    # ------------------------
    # Configuración PostgreSQL
    # ------------------------
    POSTGRESQL_DB: str
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_PORT: int
    POSTGRESQL_HOST: str

    # ------------------------
    # Configuración JWT
    # ------------------------
    JWT_SECRET_KEY: str
    JWT_ALG: str = "HS256"  # opcional, por defecto HS256

    # ------------------------
    # Reset Password / Frontend
    # ------------------------
    PASSWORD_RESET_EXPIRES_MIN: int = 30
    # URL del front a donde enviamos el enlace de reseteo (puede ser ruta Angular)
    FRONTEND_RESET_URL: str = "http://localhost:4200/auth/reset-password"

    # ------------------------
    # Email / SMTP
    # ------------------------
    EMAIL_ENABLED: bool = False         # si False, no intentamos enviar; devolvemos token/URL en la API
    SMTP_HOST: str = ""                 # p.ej. smtp.gmail.com
    SMTP_PORT: int = 587                # 587 (TLS) o 465 (SSL)
    SMTP_USER: str = ""                 # usuario SMTP (correo)
    SMTP_PASS: str = ""                 # contraseña / app password
    SMTP_FROM: str = "no-reply@example.com"
    SMTP_USE_TLS: bool = True           # True para STARTTLS (587)
    SMTP_USE_SSL: bool = False          # True para TLS implícito (465). No usar ambos a la vez.

    # ------------------------
    # Configuración n8n / upload
    # ------------------------
    N8N_WEBHOOK_URL: str
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_MB: int = 25

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
