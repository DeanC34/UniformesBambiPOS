import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from crud.crud_usuario import obtener_usuarios, crear_usuario
from utils.seguridad import verificar_password, hash_password
from utils.seguridad_usuarios import establecer_usuario


class LoginUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.configure(fg_color="#f7f2ed")  

        # Fuentes compartidas
        self.fuente_titulo = ctk.CTkFont("Bell MT", 38, "bold")
        self.fuente_label = ctk.CTkFont("Segoe UI", 16)
        self.fuente_boton = ctk.CTkFont("Sitka", 17, "bold")

        # Marco principal
        panel = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="white",
            width=460,
            height=450
        )
        panel.place(relx=0.5, rely=0.5, anchor="center")

        titulo = ctk.CTkLabel(panel, text="Acceso al Sistema", font=self.fuente_titulo)
        titulo.pack(padx = 15, pady=(25, 15))

        # ========== USUARIO ==========
        ctk.CTkLabel(panel, text="Usuario:", font=self.fuente_label).pack(pady=(10, 0))

        self.combo_usuarios = ctk.CTkComboBox(
            panel,
            values=self.cargar_nombres(),
            width=250,
            font=self.fuente_label
        )
        self.combo_usuarios.pack(pady=10)

        # Ocultar Administrador_Oficial en la lista
        # pero permitir acceso si se escribe manualmente
        self.combo_usuarios_values = [
            u for u in self.cargar_nombres() if u != "Administrador_Oficial"
        ]
        self.combo_usuarios.configure(values=self.combo_usuarios_values)

        # ========== CONTRASEÑA ==========
        ctk.CTkLabel(panel, text="Contraseña:", font=self.fuente_label).pack(pady=(15, 0))

        self.entry_pass = ctk.CTkEntry(panel, show="•", width=250, font=self.fuente_label)
        self.entry_pass.pack(pady=10)

        # ========== BOTONES ==========
        self.btn_login = ctk.CTkButton(
            panel,
            text="Ingresar",
            width=200,
            font=self.fuente_boton,
            command=self.login
        )
        self.btn_login.pack(pady=20)

        self.btn_crear = ctk.CTkButton(
            panel,
            text="Crear nuevo usuario",
            width=200,
            font=self.fuente_boton,
            fg_color="#6381c1",
            hover_color="#4e6aa6",
            command=self.popup_crear_usuario
        )
        self.btn_crear.pack(pady=(10, 5))

        # Botón para eliminar
        self.btn_eliminar = ctk.CTkButton(
            panel,
            text="Eliminar usuario",
            width=200,
            fg_color="#b85c5c",
            hover_color="#934949",
            font=self.fuente_boton,
            command=self.solicitar_admin
        )
        self.btn_eliminar.pack(pady=(5, 20))

    # ==========================================================
    def cargar_nombres(self):
        usuarios = obtener_usuarios()
        return [u["nombre_usuario"] for u in usuarios]

    # ==========================================================
    def login(self):
        usuario = self.combo_usuarios.get().strip()
        contraseña = self.entry_pass.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("Atención", "Completa todos los campos.")
            return

        usuarios = obtener_usuarios()
        usuario_data = next((u for u in usuarios if u["nombre_usuario"] == usuario), None)

        if not usuario_data:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        if not verificar_password(usuario_data["contrasena_hash"], contraseña):
            messagebox.showerror("Error", "Contraseña incorrecta.")
            return

        # Guardar usuario logueado globalmente
        establecer_usuario(usuario_data["id_usuario"], usuario_data["rol_usuario"])

        # Aquí activas el panel principal
        self.master.autenticar(usuario_data)

    # ==========================================================
    def popup_crear_usuario(self):
        ventana = ctk.CTkToplevel(self)
        ventana.geometry("380x320")
        ventana.title("Crear Usuario")
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="Nuevo usuario", font=self.fuente_titulo).pack(pady=10)

        ctk.CTkLabel(ventana, text="Usuario:").pack()
        entry_user = ctk.CTkEntry(ventana)
        entry_user.pack(pady=5)

        ctk.CTkLabel(ventana, text="Contraseña:").pack()
        entry_pass = ctk.CTkEntry(ventana, show="•")
        entry_pass.pack(pady=5)

        ctk.CTkLabel(ventana, text="Rol:").pack()
        combo_rol = ctk.CTkComboBox(ventana, values=["Empleado", "admin", "otro"])
        combo_rol.pack(pady=5)

        def crear():
            nombre = entry_user.get().strip()
            passw = entry_pass.get().strip()
            rol = combo_rol.get().strip()

            if not nombre or not passw:
                messagebox.showwarning("Atención", "Completa todos los campos.")
                return

            ok = crear_usuario(nombre, hash_password(passw), rol)
            if ok:
                messagebox.showinfo("Éxito", "Usuario creado.")
                self.refrescar_usuarios()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario.")

        ctk.CTkButton(ventana, text="Crear", command=crear).pack(pady=20)

    def refrescar_usuarios(self):
        usuarios = [u for u in self.cargar_nombres() if u != "Administrador_Oficial"]
        self.combo_usuarios.configure(values=usuarios)

    # ==========================================================
    def solicitar_admin(self):
        # Solo el Administrador_Oficial puede eliminar usuarios
        popup = ctk.CTkToplevel(self)
        popup.geometry("360x240")
        popup.title("Acceso restringido")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Ingresa credenciales de ADMIN OFICIAL").pack(pady=15)

        entry_user = ctk.CTkEntry(popup, placeholder_text="Usuario")
        entry_user.pack(pady=5)

        entry_pass = ctk.CTkEntry(popup, placeholder_text="Contraseña", show="•")
        entry_pass.pack(pady=5)

        def validar():
            user = entry_user.get()
            p = entry_pass.get()

            if user != "Administrador_Oficial":
                messagebox.showerror("Error", "Usuario inválido.")
                return

            usuarios = obtener_usuarios()
            data = next((u for u in usuarios if u["nombre_usuario"] == user), None)

            if not data or not verificar_password(data["contrasena_hash"], p):
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return

            popup.destroy()
            self.popup_eliminar_usuario()

        ctk.CTkButton(popup, text="Acceder", command=validar).pack(pady=15)

    # ==========================================================
    def popup_eliminar_usuario(self):
        ventana = ctk.CTkToplevel(self)
        ventana.geometry("380x250")
        ventana.title("Eliminar usuario")
        ventana.grab_set()

        usuarios = self.cargar_nombres()

        ctk.CTkLabel(ventana, text="Seleccionar usuario").pack(pady=10)

        combo = ctk.CTkComboBox(ventana, values=usuarios, width=200)
        combo.pack(pady=8)

        def eliminar():
            usuario = combo.get()
            if usuario == "Administrador_Oficial":
                messagebox.showwarning("Atención", "No puedes eliminar al admin oficial.")
                return

            # AQUI VA LA FUNCION eliminar_usuario(usuario)
            # …

            messagebox.showinfo("Éxito", f"Usuario '{usuario}' eliminado.")
            ventana.destroy()

        ctk.CTkButton(ventana, text="Eliminar", fg_color="#b85c5c",
                      hover_color="#934949", command=eliminar).pack(pady=20)

