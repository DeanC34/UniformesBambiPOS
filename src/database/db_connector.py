# db_connector.py
import mysql.connector
from mysql.connector import Error

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="DeanC34",   # <- tu contraseña real (puse mi nombre de usuario)
            database="uniformesbambi"
        )
        if conexion.is_connected():
            return conexion
    except Error as error:
        print(f"❌ Error al conectar con MySQL: {error}")
        return None

