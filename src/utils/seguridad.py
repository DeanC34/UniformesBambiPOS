import bcrypt

# ------------------------------------------------------------
# Genera un hash seguro para almacenar la contraseña en la BD
# ------------------------------------------------------------
def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


# ------------------------------------------------------------
# Verifica si una contraseña coincide con el hash almacenado
# ------------------------------------------------------------
def verificar_password(hashed_password: str, password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False
