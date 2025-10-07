import re
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Union
import psycopg2.extras
from app.services import Bcrypt_password, PostgresqlConexion

class Usuario(BaseModel):
    id:Optional[int] = None
    nombres: str
    apellidos: str
    email: EmailStr
    password: str
    rol: str
    
    @staticmethod
    def obtener_por_id(id: str) -> Optional["Usuario"]:
        conn = None
        try:
            conn = PostgresqlConexion.Postgresql.open()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT * FROM obtener_usuario_por_id(%s);", (id,))
            row = cursor.fetchone()
            if row:
                return Usuario.from_dict(row)
            return None
        except Exception as e:
            raise Exception(f"Error al obtener usuario: {str(e)}")
        finally:
            if conn:
                PostgresqlConexion.Postgresql.close(conn)

    @staticmethod
    def obtener_todos(cantidad,pagina) -> List[dict]:
        conn = None
        try:
            conn = PostgresqlConexion.Postgresql.open()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(
                "SELECT * FROM obtener_usuarios_todos(%s, %s);",
                (cantidad, pagina)
            )
            usuarios = cursor.fetchall()
            cursor.execute("select COUNT(*)  FROM usuario;")
            registrados = cursor.fetchone()
            return [registrados["count"],usuarios]
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")
        finally:
            if conn:
                PostgresqlConexion.Postgresql.close(conn)

    @staticmethod
    def obtener_por_email(email: str) -> Optional["Usuario"]:
        conn = None
        try:
            conn = PostgresqlConexion.Postgresql.open()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("""
                SELECT id, nombres, apellidos, email, password, rol
                FROM usuario
                WHERE email = %s;
            """, (email,))
            row = cursor.fetchone()
            if row:
                return Usuario(
                    id=row["id"],
                    nombres=row["nombres"],
                    apellidos=row["apellidos"],
                    email=row["email"],
                    password=row["password"],
                    rol=row["rol"]
                )
            return None
        except Exception as e:
            raise Exception(f"Error al obtener usuario: {str(e)}")
        finally:
            if conn:
                PostgresqlConexion.Postgresql.close(conn)

    @staticmethod
    def create(usuario: "Usuario") -> List[Union[bool, str]]:
        conn = None
        try:
            # Validar con Pydantic
            conn = PostgresqlConexion.Postgresql.open()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Verificar si el usuario ya existe
            cursor.execute("""
                SELECT id FROM usuario 
                WHERE id = %s OR email = %s
            """, (usuario.id, usuario.email))

            if cursor.fetchone():
                return [False, "Id o email ya está en uso"]

            # Hashear la contraseña
            password_hash = Bcrypt_password.generarPassword(usuario.password)

            # Insertar en la base de datos
            cursor.execute("""
                INSERT INTO usuario (nombres, apellidos, email, password, rol) 
                VALUES (%s, %s, %s, %s, %s)
            """, (
                usuario.nombres,
                usuario.apellidos,
                usuario.email,
                password_hash,
                usuario.rol
            ))

            conn.commit()
            return [True, ""]
        except Exception as e:
            print("Error al crear el usuario:", e)
            return [False, str(e)]
        finally:
            if conn:
                PostgresqlConexion.Postgresql.close(conn)

    def delete(self) -> bool:
        conn = None
        try:
            conn = PostgresqlConexion.Postgresql.open()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("DELETE FROM usuario WHERE id = %s;", (self.id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {str(e)}")
            return False
        finally:
            if conn:
                PostgresqlConexion.Postgresql.close(conn)

    def iniciarSesion(self, password: str):
        try:          
            if Bcrypt_password.verificarPassword(password, self.password):
                return True
            return False
            
        except Exception as e:
            return [False,str(e)]

    def to_dict(self):
        return {
            "id": self.id,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "email": self.email,
            "rol": self.rol}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        return cls(**data)


    ################################## VALIDACION DE LOS ATRIBUTOS ############################
    @field_validator('id')
    def validar_id(cls, i:str):
        if i <= 0:
            raise ValueError("El ID debe ser un número entero positivo.")
        return i

    @field_validator('nombres')
    def validar_nombres(cls, n: str):
        # Permitimos letras, espacios, comas y letras con tildes (á, é, í, ó, ú)
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s,]+$', n):
            raise ValueError('Los nombres solo pueden contener letras, comas, espacios y tildes.')
        return n.lower()

    @field_validator('apellidos')
    def validar_apellido(cls, a: str):
        # Permitimos letras, espacios, comas y letras con tildes (á, é, í, ó, ú)
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚ\s,]+$', a):
            raise ValueError('Los apellidos solo pueden contener letras, comas, espacios y tildes.')
        return a.lower()
    
    @field_validator('rol')
    def validar_rol(cls, rol):
        if rol not in {
                        "est-out",    # estudiante saliente
                        "coord-out",  # coordinador outgoing/saliente
                        "coord-inc",  # coordinador incoming/entrante
                        "director",   # director ori
                        "admin"       # administrador del aplicativo
                        }:
            raise ValueError(f"Rol no válido")
        return rol

    @field_validator('email')
    def validar_dominio_email(cls, value: EmailStr):
        dominio_requerido = "@udi.edu.co"
        if not value.endswith(dominio_requerido):
            raise ValueError(f"El email debe pertenecer al dominio '{dominio_requerido}'")
        return value
