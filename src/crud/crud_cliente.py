from src.database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: CLIENTE
##############################
def obtener_clientes():
    conexion = conectar_bd()
    clientes = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_cliente, nombre_cliente, telefono_cliente, correo_cliente, direccion_cliente
                FROM Cliente
                ORDER BY nombre_cliente ASC
            """)
            clientes = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo clientes: {error}")
        finally:
            cursor.close()
            conexion.close()
    return clientes

def crear_cliente(nombre, telefono, correo, direccion):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Cliente(nombre_cliente, telefono_cliente, correo_cliente, direccion_cliente)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, telefono, correo, direccion))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando cliente: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def obtener_cliente_por_id(id_cliente):
    conexion = conectar_bd()
    cliente = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_cliente, nombre_cliente, telefono_cliente, correo_cliente, direccion_cliente
                FROM Cliente
                WHERE id_cliente = %s
            """, (id_cliente,))
            cliente = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo cliente: {error}")
        finally:
            cursor.close()
            conexion.close()
    return cliente

def actualizar_cliente(id_cliente, nombre, telefono, correo, direccion):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE Cliente
                SET nombre_cliente=%s, telefono_cliente=%s, correo_cliente=%s, direccion_cliente=%s
                WHERE id_cliente=%s
            """
            cursor.execute(sql, (nombre, telefono, correo, direccion, id_cliente))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando cliente: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_cliente(id_cliente):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Cliente WHERE id_cliente=%s", (id_cliente,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando cliente: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
