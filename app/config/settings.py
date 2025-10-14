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

    # ------------------------
    # Configuración n8n / upload
    # ------------------------
    N8N_WEBHOOK_URL: str
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_MB: int = 25

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"   # <--- esto hace que ignore variables no declaradas

settings = Settings()
