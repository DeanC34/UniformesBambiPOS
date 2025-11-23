from src.database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: VENTADETALLE
##############################
def obtener_detalles_venta():
    conexion = conectar_bd()
    detalles = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_detalle, cantidad, precio_unitario, VariacionProducto_id_variacion, Venta_id_venta
                FROM VentaDetalle
                ORDER BY id_detalle ASC
            """)
            detalles = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo detalles de venta: {error}")
        finally:
            cursor.close()
            conexion.close()
    return detalles

def crear_detalle_venta(cantidad, precio_unitario, variacion_id, venta_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO VentaDetalle(cantidad, precio_unitario, VariacionProducto_id_variacion, Venta_id_venta)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (cantidad, precio_unitario, variacion_id, venta_id))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando detalle de venta: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def obtener_detalle_por_id(id_detalle):
    conexion = conectar_bd()
    detalle = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_detalle, cantidad, precio_unitario, VariacionProducto_id_variacion, Venta_id_venta
                FROM VentaDetalle
                WHERE id_detalle=%s
            """, (id_detalle,))
            detalle = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo detalle de venta: {error}")
        finally:
            cursor.close()
            conexion.close()
    return detalle

def actualizar_detalle_venta(id_detalle, cantidad, precio_unitario, variacion_id, venta_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE VentaDetalle
                SET cantidad=%s, precio_unitario=%s, VariacionProducto_id_variacion=%s, Venta_id_venta=%s
                WHERE id_detalle=%s
            """
            cursor.execute(sql, (cantidad, precio_unitario, variacion_id, venta_id, id_detalle))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando detalle de venta: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_detalle_venta(id_detalle):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM VentaDetalle WHERE id_detalle=%s", (id_detalle,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando detalle de venta: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()