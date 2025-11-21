from src.database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: VENTA
##############################
def obtener_ventas():
    conexion = conectar_bd()
    ventas = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_venta, fecha_venta, total_venta, Cliente_id_cliente
                FROM Venta
                ORDER BY id_venta ASC
            """)
            ventas = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo ventas: {error}")
        finally:
            cursor.close()
            conexion.close()
    return ventas

def crear_venta(fecha, total, cliente_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Venta(fecha_venta, total_venta, Cliente_id_cliente)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (fecha, total, cliente_id))
            conexion.commit()
            return cursor.lastrowid  # devolvemos el id de la venta creada
        except Error as error:
            print(f"❌ Error creando venta: {error}")
            return None
        finally:
            cursor.close()
            conexion.close()

def obtener_venta_por_id(id_venta):
    conexion = conectar_bd()
    venta = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_venta, fecha_venta, total_venta, Cliente_id_cliente
                FROM Venta
                WHERE id_venta=%s
            """, (id_venta,))
            venta = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo venta: {error}")
        finally:
            cursor.close()
            conexion.close()
    return venta

def actualizar_venta(id_venta, fecha, total, cliente_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE Venta
                SET fecha_venta=%s, total_venta=%s, Cliente_id_cliente=%s
                WHERE id_venta=%s
            """
            cursor.execute(sql, (fecha, total, cliente_id, id_venta))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando venta: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_venta(id_venta):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Venta WHERE id_venta=%s", (id_venta,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando venta: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()