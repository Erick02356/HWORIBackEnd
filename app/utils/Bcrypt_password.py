import bcrypt
def generarPassword(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verificarPassword(password_plana: str, password_hasheada: str) -> bool:
    try:
        return bcrypt.checkpw(
            password_plana.encode('utf-8'),
            password_hasheada.encode('utf-8')
            )
    except:
        return False