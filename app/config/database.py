from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 🔹 Configura tu conexión (ajústala según tu entorno)
DB_USER = os.getenv("POSTGRESQL_USER")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
DB_HOST = os.getenv("POSTGRESQL_HOST")
DB_PORT = os.getenv("POSTGRESQL_PORT")
DB_NAME = os.getenv("POSTGRESQL_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 🔹 Crea el motor (equivalente al DataSource de Spring)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 🔹 Crea la sesión (equivalente al EntityManager)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Clase base para tus modelos (equivalente a @Entity)
Base = declarative_base()

# 🔹 Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
