from database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: PRODUCTO
##############################

def obtener_productos():
    conexion = conectar_bd()
    productos = []

    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_producto, nombre_producto, descripcion_producto,
                       categoria, precio, estado
                FROM Producto
                ORDER BY nombre_producto ASC
            """)
            productos = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo productos: {error}")
        finally:
            cursor.close()
            conexion.close()

    return productos


def crear_producto(nombre, descripcion, categoria, precio, estado):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Producto(nombre_producto, descripcion_producto, categoria, precio, estado)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, descripcion, categoria, precio, estado))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando producto: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()


def obtener_producto_por_id(id_producto):
    conexion = conectar_bd()
    producto = None

    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_producto, nombre_producto, descripcion_producto,
                       categoria, precio, estado
                FROM Producto
                WHERE id_producto = %s
            """, (id_producto,))
            producto = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo producto: {error}")
        finally:
            cursor.close()
            conexion.close()

    return producto


def actualizar_producto(id_producto, nombre, descripcion, categoria, precio, estado):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE Producto
                SET nombre_producto = %s,
                    descripcion_producto = %s,
                    categoria = %s,
                    precio = %s,
                    estado = %s
                WHERE id_producto = %s
            """
            cursor.execute(sql, (nombre, descripcion, categoria, precio, estado, id_producto))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando producto: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()


def eliminar_producto(id_producto):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM Producto WHERE id_producto = %s", (id_producto,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando producto: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
