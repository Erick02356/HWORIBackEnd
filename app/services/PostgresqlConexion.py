import os
from psycopg2 import pool
import sys
class Postgresql:
    _pool = None
    @classmethod
    def iniciar_pool(cls, minconn=2, maxconn=15):
        if cls._pool is None:
            
            try:
                cls._pool = pool.SimpleConnectionPool(
                    minconn,
                    maxconn,
                    dbname= os.getenv("POSTGRESQL_DB"),
                    user=os.getenv("POSTGRESQL_USER"),
                    password=os.getenv("POSTGRESQL_PASSWORD"),
                    host=os.getenv("POSTGRESQL_HOST")
                )
                
                print("Pool de conexiones inicializado.")
            except Exception as e:
                print(f"Error al iniciar el pool de conexiones: {e}")

    @classmethod
    def open(cls):
        if cls._pool is None:
            raise Exception("El pool no está inicializado. Llama a iniciar_pool() primero.")
        return cls._pool.getconn()

    @classmethod
    def close(cls, conn):
        if cls._pool and conn:
            cls._pool.putconn(conn)

    @classmethod
    def cerrar_pool(cls):
        if cls._pool:
            cls._pool.closeall()
            print("Pool de conexiones cerrado.")
