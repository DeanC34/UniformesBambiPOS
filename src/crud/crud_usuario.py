from src.database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: USUARIO
##############################

def obtener_usuarios():
    conexion = conectar_bd()
    usuarios = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_usuario, nombre_usuario, rol_usuario
                FROM Usuario
                ORDER BY nombre_usuario ASC
            """)
            usuarios = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo usuarios: {error}")
        finally:
            cursor.close()
            conexion.close()
    return usuarios


def crear_usuario(nombre, contraseña_hash, rol):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Usuario(nombre_usuario, contraseña_hash, rol_usuario)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (nombre, contraseña_hash, rol))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando usuario: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()


def obtener_usuario_por_id(id_usuario):
    conexion = conectar_bd()
    usuario = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_usuario, nombre_usuario, rol_usuario
                FROM Usuario
                WHERE id_usuario=%s
            """, (id_usuario,))
            usuario = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo usuario: {error}")
        finally:
            cursor.close()
            conexion.close()
    return usuario
