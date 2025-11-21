from src.database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: VARIACIONPRODUCTO
##############################
def obtener_variaciones():
    conexion = conectar_bd()
    variaciones = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_variacion, talla, color, stock, Producto_id_producto
                FROM VariacionProducto
                ORDER BY id_variacion ASC
            """)
            variaciones = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo variaciones: {error}")
        finally:
            cursor.close()
            conexion.close()
    return variaciones

def crear_variacion(talla, color, stock, producto_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO VariacionProducto(talla, color, stock, Producto_id_producto)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (talla, color, stock, producto_id))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando variación: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def obtener_variacion_por_id(id_variacion):
    conexion = conectar_bd()
    variacion = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_variacion, talla, color, stock, Producto_id_producto
                FROM VariacionProducto
                WHERE id_variacion = %s
            """, (id_variacion,))
            variacion = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo variación: {error}")
        finally:
            cursor.close()
            conexion.close()
    return variacion

def actualizar_variacion(id_variacion, talla, color, stock, producto_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE VariacionProducto
                SET talla = %s, color = %s, stock = %s, Producto_id_producto = %s
                WHERE id_variacion = %s
            """
            cursor.execute(sql, (talla, color, stock, producto_id, id_variacion))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando variación: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_variacion(id_variacion):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM VariacionProducto WHERE id_variacion = %s", (id_variacion,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando variación: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
