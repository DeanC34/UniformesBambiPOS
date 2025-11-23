import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from src.crud.crud_empleado import *
from src.crud.crud_usuario import obtener_usuarios  # asumo que este método existe y devuelve lista de dicts

class EmpleadosUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # Fuente elegante global
        self.fuente_titulo = ctk.CTkFont("Segoe UI", 26, "bold")
        self.fuente_subtitulo = ctk.CTkFont("Segoe UI", 18, "bold")
        self.fuente_normal = ctk.CTkFont("Segoe UI", 14)
        self.fuente_popup = ctk.CTkFont("Segoe UI", 16)
        self.fuente_menu = ctk.CTkFont("Segoe UI", 15, "bold")

        self.pack(fill="both", expand=True)

        # ---------- SIDEBAR LATERAL DESPLEGABLE ----------
        self.sidebar_visible = False

        self.sidebar = ctk.CTkFrame(
            self,
            width=300,
            fg_color="#21416B"   # dark-blue
        )

        # Sidebar inicialmente fuera del canvas (oculta a la izquierda)
        self.sidebar.place(
            x=-300,               # completamente fuera a la izquierda
            y=80,                 # NO tapa el botón
            relheight=1           # ocupa toda la altura restante
        )

        self.sidebar.lift()
        self.sidebar.grid(row=0, column=0, rowspan=10, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_remove()

        menu_items = [
            "Inicio",
            "Empleado",
            "Ventas",
            "Clientes",
            "Proveedores",
            "Compras",
            "Opciones",
            "Acerca de"
        ]

        for item in menu_items:
            b = ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                hover_color="#142944",
                text_color="white",
                font=self.fuente_menu,
                corner_radius=0,
                height=45,
                anchor="w"
            )
            b.pack(fill="x", pady=2, padx=8)

        # Botón para abrir/cerrar
        self.menu_toggle = ctk.CTkButton(
            self,
            text="≡",
            width=50,
            height=40,
            fg_color="#21416B",
            hover_color="#1A1A40",
            text_color="white",
            font=("Segoe UI", 20, "bold"),
            command=self.toggle_sidebar
        )
        self.menu_toggle.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Ajuste del layout principal
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        # ---------- TÍTULO PRINCIPAL ----------
        title = ctk.CTkLabel(self, text="Gestión de Empleados", font=self.fuente_titulo)
        title.grid(row=1, column=0, columnspan=2, pady=20, sticky="n")

        # ---------- ESTILO TABLA OSCURA ----------
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1a1a1a",
            foreground="white",
            rowheight=30,
            fieldbackground="#1a1a1a"
        )
        style.configure(
            "Treeview.Heading",
            background="#333333",
            foreground="white",
            font=("Segoe UI", 12, "bold")
        )
        style.map("Treeview", background=[("selected", "#444")])

        # ---------- TABLA ----------
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Puesto", "Teléfono", "Rol", "Usuario"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Puesto", text="Puesto")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Usuario", text="Usuario")

        # columnas anchos recomendados
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nombre", width=220)
        self.tree.column("Puesto", width=150)
        self.tree.column("Teléfono", width=120, anchor="center")
        self.tree.column("Rol", width=100, anchor="center")
        self.tree.column("Usuario", width=180)

        self.tree.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=0, sticky="nse")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # ============================================================
        #  ÁREA DE INTERACCIÓN (botones)
        # ============================================================
        interaccion_title = ctk.CTkLabel(self, text="Área de Interacción", font=self.fuente_subtitulo)
        interaccion_title.grid(row=2, column=1, sticky="n", pady=(10, 0))

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=2, column=1, padx=10, pady=(40, 0), sticky="nsew")
        btn_frame.grid_rowconfigure((0,1,2,3), weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)

        btn_style = {
            "width": 140,
            "height": 40,
            "fg_color": "#21416B",
            "hover_color": "#142944",
            "text_color": "white",
            "corner_radius": 10,
            "font": self.fuente_normal
        }

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_empleado, **btn_style).grid(row=0, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.confirmar_actualizacion_popup, **btn_style).grid(row=1, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.confirmar_eliminacion_popup, **btn_style).grid(row=2, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.mostrar_empleados, **btn_style).grid(row=3, column=0, pady=10, sticky="nsew")

        # ============================================================
        #  ÁREA DE CAMPOS
        # ============================================================
        campos_title = ctk.CTkLabel(self, text="Área de Campos", font=self.fuente_subtitulo)
        campos_title.grid(row=3, column=0, columnspan=2, sticky="n", pady=(10, 0))

        form = ctk.CTkFrame(self)
        form.grid(row=3, column=0, columnspan=2, pady=(40,10), padx=10, sticky="nsew")
        for i in range(2):
            form.grid_columnconfigure(i, weight=1)

        # Campos del formulario
        self.nombre = ctk.CTkEntry(form, placeholder_text="Nombre", font=self.fuente_normal)
        self.nombre.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.puesto = ctk.CTkEntry(form, placeholder_text="Puesto", font=self.fuente_normal)
        self.puesto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.telefono = ctk.CTkEntry(form, placeholder_text="Teléfono", font=self.fuente_normal)
        self.telefono.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # OptionMenu Rol
        self.rol = ctk.CTkOptionMenu(form, values=["admin", "vendedor", "otro"], font=self.fuente_normal)
        self.rol.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # OptionMenu Usuario (lista formateada "id - nombre (rol)")
        usuarios_list = self._cargar_usuarios_para_optionmenu()
        self.usuario_option = ctk.CTkOptionMenu(form, values=usuarios_list, font=self.fuente_normal)
        self.usuario_option.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # campo oculto id seleccionado
        self.id_seleccionado = None

        # enlazar selección de tabla
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # cargar inicialmente
        self.mostrar_empleados()

    # -------------------------
    # helpers / util
    # -------------------------
    def _cargar_usuarios_para_optionmenu(self):
        try:
            usuarios = obtener_usuarios()  # se espera lista de dicts: id_usuario, nombre_usuario, rol_usuario
        except Exception:
            usuarios = []

        valores = []
        for u in usuarios:
            uid = u.get("id_usuario", "")
            nombre = u.get("nombre_usuario", "")
            rol = u.get("rol_usuario", "")
            valores.append(f"{uid} - {nombre} ({rol})")
        # al menos un valor por defecto
        if not valores:
            valores = ["0 - (sin usuarios)"]
        return valores

    def popup(self, titulo, mensaje):
        win = ctk.CTkToplevel(self)
        win.title(titulo)
        win.geometry("360x160")
        win.resizable(False, False)
        win.grab_set()
        ctk.CTkLabel(win, text=mensaje, font=self.fuente_popup).pack(pady=16)
        ctk.CTkButton(win, text="Cerrar", fg_color="#21416B", hover_color="#142944", command=win.destroy, font=self.fuente_normal).pack(pady=10)

    # -------------------------
    # VALIDACIONES
    # -------------------------
    def validar_campos(self):
        if not self.nombre.get().strip():
            return "El campo NOMBRE está vacío."
        if not self.puesto.get().strip():
            return "El campo PUESTO está vacío."
        # teléfono opcional
        return None

    # -------------------------
    # CRUD real usando src/crud/crud_empleado.py
    # -------------------------
    def mostrar_empleados(self):
        # limpiar
        for r in self.tree.get_children():
            self.tree.delete(r)

        try:
            empleados = obtener_empleados()
        except Exception as e:
            print("Error obtener_empleados:", e)
            empleados = []

        for e in empleados:
            usuario_id = e.get("Usuario_id_usuario")
            # mostrar usuario como 'id' (si existe)
            usuario_text = str(usuario_id) if usuario_id else ""
            self.tree.insert("", "end", values=(
                e.get("id_empleado"),
                e.get("nombre_empleado"),
                e.get("puesto_empleado"),
                e.get("telefono_empleado"),
                e.get("rol_empleado"),
                usuario_text
            ))

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        id_empleado = item["values"][0]
        # obtener datos completos
        empleado = obtener_empleado_por_id(id_empleado)
        if not empleado:
            return

        self.id_seleccionado = id_empleado
        self.nombre.delete(0, "end")
        self.nombre.insert(0, empleado.get("nombre_empleado", "") or "")

        self.puesto.delete(0, "end")
        self.puesto.insert(0, empleado.get("puesto_empleado", "") or "")

        self.telefono.delete(0, "end")
        self.telefono.insert(0, empleado.get("telefono_empleado", "") or "")

        rol_val = empleado.get("rol_empleado", "") or "vendedor"
        # ajustar rol option
        try:
            self.rol.set(rol_val)
        except Exception:
            pass

        # ajustar usuario option: si tiene Usuario_id_usuario, seleccionar la opción formateada
        uid = empleado.get("Usuario_id_usuario")
        if uid:
            # construir label tal cual la OptionMenu (buscar en sus valores)
            values = self.usuario_option._options if hasattr(self.usuario_option, "_options") else self.usuario_option.cget("values")
            # generar target like "id - name (rol)" pero si no encontramos nombre/rol solo con id
            target = None
            try:
                usuarios = obtener_usuarios()
                for u in usuarios:
                    if u.get("id_usuario") == uid:
                        target = f"{u.get('id_usuario')} - {u.get('nombre_usuario')} ({u.get('rol_usuario')})"
                        break
            except Exception:
                target = None
            if target:
                try:
                    self.usuario_option.set(target)
                except Exception:
                    pass
            else:
                # fallback: set to id
                try:
                    self.usuario_option.set(str(uid))
                except Exception:
                    pass
        else:
            # no tiene usuario asignado
            try:
                self.usuario_option.set(self.usuario_option.cget("values")[0])
            except Exception:
                pass

    def crear_empleado(self):
        error = self.validar_campos()
        if error:
            self.popup("Error", error)
            return

        nombre = self.nombre.get().strip()
        puesto = self.puesto.get().strip()
        telefono = self.telefono.get().strip()
        rol = self.rol.get().strip()

        # Usuario: extraer id si la opción sigue formato "id - name (rol)"
        usuario_raw = self.usuario_option.get()
        usuario_id = None
        try:
            usuario_id = int(usuario_raw.split(" - ")[0])
        except Exception:
            usuario_id = None

        ok = crear_empleado(nombre, puesto, telefono, rol, usuario_id)
        if ok:
            self.popup("Éxito", "Empleado creado correctamente.")
            self.mostrar_empleados()
        else:
            self.popup("Error", "No se pudo crear el empleado.")

    def confirmar_actualizacion_popup(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un empleado primero.")
            return

        error = self.validar_campos()
        if error:
            self.popup("Error", error)
            return

        # obtener nombre del empleado para mostrar
        nombre = self.nombre.get().strip() or "(sin nombre)"
        win = ctk.CTkToplevel(self)
        win.title("Confirmar actualización")
        win.geometry("380x170")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text=f"¿Estás seguro de actualizar ID: {self.id_seleccionado}\nNombre: {nombre}?", font=self.fuente_popup).pack(pady=16)

        ctk.CTkButton(win, text="Confirmar", fg_color="#21416B", hover_color="#142944",
                      command=lambda: [self._do_update_and_close(win)], font=self.fuente_normal).pack(pady=6)
        ctk.CTkButton(win, text="Cancelar", fg_color="#333", hover_color="#222", command=win.destroy, font=self.fuente_normal).pack(pady=4)

    def _do_update_and_close(self, win):
        self.actualizar_empleado()
        win.destroy()

    def actualizar_empleado(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un empleado primero.")
            return

        error = self.validar_campos()
        if error:
            self.popup("Error", error)
            return

        nombre = self.nombre.get().strip()
        puesto = self.puesto.get().strip()
        telefono = self.telefono.get().strip()
        rol = self.rol.get().strip()

        usuario_raw = self.usuario_option.get()
        usuario_id = None
        try:
            usuario_id = int(usuario_raw.split(" - ")[0])
        except Exception:
            usuario_id = None

        ok = actualizar_empleado(self.id_seleccionado, nombre, puesto, telefono, rol, usuario_id)
        if ok:
            self.popup("Éxito", "Empleado actualizado correctamente.")
            self.mostrar_empleados()
        else:
            self.popup("Error", "No se pudo actualizar el empleado.")

    def confirmar_eliminacion_popup(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un empleado primero.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Confirmar eliminación")
        win.geometry("360x160")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text="¿Eliminar el empleado seleccionado?", font=self.fuente_popup).pack(pady=16)
        ctk.CTkButton(win, text="Sí, eliminar", fg_color="#8b0000", hover_color="#5a0000",
                      command=lambda: [self._do_delete_and_close(win)], font=self.fuente_normal).pack(pady=6)
        ctk.CTkButton(win, text="Cancelar", fg_color="#333", hover_color="#222", command=win.destroy, font=self.fuente_normal).pack(pady=4)

    def _do_delete_and_close(self, win):
        self.eliminar_empleado_confirmado()
        win.destroy()

    def eliminar_empleado_confirmado(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un empleado primero.")
            return

        ok = eliminar_empleado(self.id_seleccionado)
        if ok:
            self.popup("Éxito", "Empleado eliminado.")
            self.mostrar_empleados()
            self.id_seleccionado = None
            # limpiar campos
            self.nombre.delete(0, "end")
            self.puesto.delete(0, "end")
            self.telefono.delete(0, "end")
        else:
            self.popup("Error", "No se pudo eliminar el empleado.")

    # ============================================================
    #  SIDEBAR OVERLAY (slide con place)
    # ============================================================
    def toggle_sidebar(self):
        if self.sidebar_visible:
            # Ocultar (slide hacia la izquierda)
            for x in range(0, 301, 20):
                self.sidebar.place(x=0 - x, y=80)
                self.sidebar.update()
            self.sidebar_visible = False
        else:
            # Mostrar (slide hacia la derecha)
            self.sidebar.lift()
            for x in range(-300, 1, 20):
                self.sidebar.place(x=x, y=80)
                self.sidebar.update()
            self.sidebar_visible = True
