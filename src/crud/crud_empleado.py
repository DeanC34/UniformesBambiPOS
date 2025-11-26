from database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: EMPLEADO
##############################
def obtener_empleados():
    conexion = conectar_bd()
    empleados = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_empleado, nombre_empleado, puesto_empleado, telefono_empleado, rol_empleado, Usuario_id_usuario
                FROM Empleado
                ORDER BY nombre_empleado ASC
            """)
            empleados = cursor.fetchall()
        except Error as error:
            print(f"❌ Error obteniendo empleados: {error}")
        finally:
            cursor.close()
            conexion.close()
    return empleados

def crear_empleado(nombre, puesto, telefono, rol, usuario_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Empleado(nombre_empleado, puesto_empleado, telefono_empleado, rol_empleado, Usuario_id_usuario)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, puesto, telefono, rol, usuario_id))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando empleado: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def obtener_empleado_por_id(id_empleado):
    conexion = conectar_bd()
    empleado = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_empleado, nombre_empleado, puesto_empleado, telefono_empleado, rol_empleado, Usuario_id_usuario
                FROM Empleado
                WHERE id_empleado=%s
            """, (id_empleado,))
            empleado = cursor.fetchone()
        except Error as error:
            print(f"❌ Error obteniendo empleado: {error}")
        finally:
            cursor.close()
            conexion.close()
    return empleado

def actualizar_empleado(id_empleado, nombre, puesto, telefono, rol, usuario_id):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE Empleado
                SET nombre_empleado=%s, puesto_empleado=%s, telefono_empleado=%s, rol_empleado=%s, Usuario_id_usuario=%s
                WHERE id_empleado=%s
            """
            cursor.execute(sql, (nombre, puesto, telefono, rol, usuario_id, id_empleado))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando empleado: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()

def eliminar_empleado(id_empleado):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Empleado WHERE id_empleado=%s", (id_empleado,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando empleado: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()