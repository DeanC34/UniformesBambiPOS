# seguridad_usuarios.py

usuario_actual = {
    "id_usuario": None,
    "rol_usuario": None
}

def establecer_usuario(id_usuario, rol_usuario):
    usuario_actual["id_usuario"] = id_usuario
    usuario_actual["rol_usuario"] = rol_usuario
