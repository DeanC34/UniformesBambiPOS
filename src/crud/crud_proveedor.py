from database.db_connector import conectar_bd
from mysql.connector import Error

##############################
# CRUD TABLA: PROVEEDOR
##############################

def obtener_proveedores():
    conexion = conectar_bd()
    proveedores = []
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_proveedor, nombre_proveedor, telefono_proveedor, correo_proveedor, direccion_proveedor
                FROM Proveedor
                ORDER BY nombre_proveedor ASC
            """)

            datos = cursor.fetchall()

            # Normalizar claves
            proveedores = [
                {
                    "id_proveedor": p["id_proveedor"],
                    "nombre": p["nombre_proveedor"],
                    "telefono": p["telefono_proveedor"],
                    "correo": p["correo_proveedor"],
                    "direccion": p["direccion_proveedor"]
                }
                for p in datos
            ]

        except Error as error:
            print(f"❌ Error obteniendo proveedores: {error}")
        finally:
            cursor.close()
            conexion.close()
    return proveedores


def crear_proveedor(nombre, telefono, correo, direccion):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Proveedor(nombre_proveedor, telefono_proveedor, correo_proveedor, direccion_proveedor)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, telefono, correo, direccion))
            conexion.commit()
            return True
        except Error as error:
            print(f"❌ Error creando proveedor: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()


def obtener_proveedor_por_id(id_proveedor):
    conexion = conectar_bd()
    proveedor = None
    if conexion:
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_proveedor, nombre_proveedor, telefono_proveedor, correo_proveedor, direccion_proveedor
                FROM Proveedor
                WHERE id_proveedor=%s
            """, (id_proveedor,))

            p = cursor.fetchone()
            if p:
                proveedor = {
                    "id_proveedor": p["id_proveedor"],
                    "nombre": p["nombre_proveedor"],
                    "telefono": p["telefono_proveedor"],
                    "correo": p["correo_proveedor"],
                    "direccion": p["direccion_proveedor"]
                }

        except Error as error:
            print(f"❌ Error obteniendo proveedor: {error}")
        finally:
            cursor.close()
            conexion.close()
    return proveedor


def actualizar_proveedor(id_proveedor, nombre, telefono, correo, direccion):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE Proveedor
                SET nombre_proveedor=%s, telefono_proveedor=%s, correo_proveedor=%s, direccion_proveedor=%s
                WHERE id_proveedor=%s
            """
            cursor.execute(sql, (nombre, telefono, correo, direccion, id_proveedor))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error actualizando proveedor: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()


def eliminar_proveedor(id_proveedor):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Proveedor WHERE id_proveedor=%s", (id_proveedor,))
            conexion.commit()
            return cursor.rowcount > 0
        except Error as error:
            print(f"❌ Error eliminando proveedor: {error}")
            return False
        finally:
            cursor.close()
            conexion.close()
