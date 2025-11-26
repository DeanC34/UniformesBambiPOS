from database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: DEFECTO PRODUCTO
##############################

def obtener_defectos():
    conexion = conectar_bd()
    defectos = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_defecto, descripcion_defecto, fecha_defecto, VariacionProducto_id_variacion, Empleado_id_empleado
                FROM DefectoProducto
                ORDER BY id_defecto ASC
            """)
            defectos = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo defectos de producto: {error}")
        finally:
            cursor.close()
            conexion.close()
    return defectos

def crear_defecto(descripcion, fecha, variacion_id, empleado_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO DefectoProducto(descripcion_defecto, fecha_defecto, VariacionProducto_id_variacion, Empleado_id_empleado)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (descripcion, fecha, variacion_id, empleado_id))
            conexion.commit()
            return cursor.lastrowid
        except Error as error:
            print(f"❌ Error creando defecto de producto: {error}")
            return None
        finally:
            cursor.close()
            conexion.close()

def obtener_defecto_por_id(id_defecto):
    conexion = conectar_bd()
    defecto = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_defecto, descripcion_defecto, fecha_defecto, VariacionProducto_id_variacion, Empleado_id_empleado
                FROM DefectoProducto
                WHERE id_defecto=%s
            """, (id_defecto,))
            defecto = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo defecto de producto: {error}")
        finally:
            cursor.close()
            conexion.close()
    return defecto

def actualizar_defecto(id_defecto, descripcion, fecha, variacion_id, empleado_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE DefectoProducto
                SET descripcion_defecto=%s, fecha_defecto=%s, VariacionProducto_id_variacion=%s, Empleado_id_empleado=%s
                WHERE id_defecto=%s
            """
            cursor.execute(sql, (descripcion, fecha, variacion_id, empleado_id, id_defecto))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando defecto de producto: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_defecto(id_defecto):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM DefectoProducto WHERE id_defecto=%s", (id_defecto,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando defecto de producto: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()