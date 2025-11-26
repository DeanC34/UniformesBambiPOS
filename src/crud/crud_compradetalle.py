from database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: COMPRADETALLE
##############################
def obtener_detalles_compra():
    conexion = conectar_bd()
    detalles = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_compra_detalle, cantidad, preciounitario, VariacionProducto_id_variacion, Compra_id_compra
                FROM CompraDetalle
                ORDER BY id_compra_detalle ASC
            """)
            detalles = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo detalles de compra: {error}")
        finally:
            cursor.close()
            conexion.close()
    return detalles

def crear_detalle_compra(cantidad, preciounitario, variacion_id, compra_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO CompraDetalle(cantidad, preciounitario, VariacionProducto_id_variacion, Compra_id_compra)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (cantidad, preciounitario, variacion_id, compra_id))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando detalle de compra: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def obtener_detalle_compra_por_id(id_detalle):
    conexion = conectar_bd()
    detalle = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_compra_detalle, cantidad, preciounitario, VariacionProducto_id_variacion, Compra_id_compra
                FROM CompraDetalle
                WHERE id_compra_detalle=%s
            """, (id_detalle,))
            detalle = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo detalle de compra: {error}")
        finally:
            cursor.close()
            conexion.close()
    return detalle

def actualizar_detalle_compra(id_detalle, cantidad, preciounitario, variacion_id, compra_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE CompraDetalle
                SET cantidad=%s, preciounitario=%s, VariacionProducto_id_variacion=%s, Compra_id_compra=%s
                WHERE id_compra_detalle=%s
            """
            cursor.execute(sql, (cantidad, preciounitario, variacion_id, compra_id, id_detalle))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando detalle de compra: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_detalle_compra(id_detalle):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM CompraDetalle WHERE id_compra_detalle=%s", (id_detalle,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando detalle de compra: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()