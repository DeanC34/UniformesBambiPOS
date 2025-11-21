from src.database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: COMPRA
##############################
def obtener_compras():
    conexion = conectar_bd()
    compras = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_compra, fecha_compra, total_compra, Proveedor_id_proveedor
                FROM Compra
                ORDER BY id_compra ASC
            """)
            compras = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo compras: {error}")
        finally:
            cursor.close()
            conexion.close()
    return compras

def crear_compra(fecha, total, proveedor_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Compra(fecha_compra, total_compra, Proveedor_id_proveedor)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (fecha, total, proveedor_id))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando compra: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def obtener_compra_por_id(id_compra):
    conexion = conectar_bd()
    compra = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_compra, fecha_compra, total_compra, Proveedor_id_proveedor
                FROM Compra
                WHERE id_compra=%s
            """, (id_compra,))
            compra = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo compra: {error}")
        finally:
            cursor.close()
            conexion.close()
    return compra

def actualizar_compra(id_compra, fecha, total, proveedor_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE Compra
                SET fecha_compra=%s, total_compra=%s, Proveedor_id_proveedor=%s
                WHERE id_compra=%s
            """
            cursor.execute(sql, (fecha, total, proveedor_id, id_compra))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando compra: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_compra(id_compra):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Compra WHERE id_compra=%s", (id_compra,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando compra: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()