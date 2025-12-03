import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from crud.crud_cliente import *

class ClientesUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # Fuente elegante global
        self.fuente_titulo = ctk.CTkFont("Bell MT", 26, "bold")
        self.fuente_subtitulo = ctk.CTkFont("Bell MT", 22, "bold")
        self.fuente_normal = ctk.CTkFont("Segoe UI", 14)
        self.fuente_popup = ctk.CTkFont("Segoe UI", 16)
        self.fuente_menu = ctk.CTkFont("Sitka", 17, "bold")

        self.grid(row=0, column=0, sticky="nsew")

        # ---------- SIDEBAR LATERAL DESPLEGABLE ----------
        self.sidebar_visible = False

        self.sidebar = ctk.CTkFrame(
            self,
            width=300,
            fg_color="#825c46"
        )

        # Sidebar inicialmente fuera del canvas (oculta a la izquierda)
        self.sidebar.place(x=-300, y=120)

        # Truco para que NO afecte el grid del resto de widgets
        self.sidebar.lift()
        #self.sidebar.grid(row=0, column=0, rowspan=50, sticky="nsw")
        #self.sidebar.grid_propagate(False)
        #self.sidebar.grid_remove()  # Sin esto, tapa todo

        menu_items = [
            "Inicio",
            "Productos",
            "Empleado",
            "Ventas",
            "Clientes",
            "Proveedores",
            "Compras",
            "Opciones",
            "Acerca de"
        ]

        PROHIBIDOS_EMPLEADO = ["Empleado", "Compras", "Proveedores"]
        rol = self.master.usuario_actual.get("rol_usuario", "otro")
        es_empleado = rol != "admin"

        for item in menu_items:
            def accion(n=item):
                if es_empleado and n in PROHIBIDOS_EMPLEADO:
                    messagebox.showwarning(
                        "Acceso restringido",
                        f"No tienes permisos para acceder a {n}."
                    )
                    return

                self.master.mostrar_pantalla(n)

            b = ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                hover_color="#644736",
                text_color="white",
                font=self.fuente_menu,
                corner_radius=0,
                height=45,
                anchor="w",
                command=accion  # ← ahora realmente llama a la lógica de permisos
                )
            b.pack(fill="x", pady=2, padx=8)


        # Botón para abrir/cerrar
        self.menu_toggle = ctk.CTkButton(
            self,
            text="≡",
            width=50,
            height=40,
            fg_color="#825c46",
            hover_color="#644736",
            text_color="white",
            font=("Segoe UI", 20, "bold"),
            command=self.toggle_sidebar
        )
        self.menu_toggle.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Ajuste del layout principal - orden de renderizacion fila y columna
        self.grid_rowconfigure(0, weight=0)  # Botón menú
        self.grid_rowconfigure(1, weight=0)  # Titulo principal
        self.grid_rowconfigure(2, weight=5)  # Área de Interacción (título + botones)
        self.grid_rowconfigure(3, weight=1)  # Tabla (solo la tabla)

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        # ---------- TÍTULO PRINCIPAL ----------
        title = ctk.CTkLabel(self, text="Gestión de Clientes", font=self.fuente_titulo)
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # ---------- ESTILO TABLA OSCURA ----------
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2c2517",
            foreground="white",
            rowheight=30,
            fieldbackground="#312b21"
        )
        style.configure(
            "Treeview.Heading",
            background="#333333",
            foreground="white",
            font=("Segoe UI", 12, "bold")
        )
        style.map("Treeview", background=[("selected", "#444")])

        # ---- CONTENEDOR PARA LA TABLA ----
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        # El frame de la tabla debe poder crecer
        self.tabla_frame.grid_rowconfigure(0, weight=1)
        self.tabla_frame.grid_columnconfigure(0, weight=1)
        self.tabla_frame.grid_columnconfigure(1, weight=0)

        # ---------- TABLA ----------
        self.tree = ttk.Treeview(self.tabla_frame, columns=("ID", "Nombre", "Teléfono", "Correo", "Dirección"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Dirección", text="Dirección")

        # columnas anchos recomendados
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nombre", width=220)
        self.tree.column("Teléfono", width=140, anchor="center")
        self.tree.column("Correo", width=200)
        self.tree.column("Dirección", width=300)

        # ---- TABLA (fila 1) ----
        self.tree.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Scrollbar estilizada usando CTkScrollbar
        try:
            scrollbar = ctk.CTkScrollbar(
                self.tabla_frame,
                command=self.tree.yview,
                width=14,
                fg_color="#644736",
                button_color="#825c46",
                button_hover_color="#4E382B"
            )
            # ---- SCROLLBAR (fila 1, otra columna) ----
            scrollbar.grid(row=1, column=1, sticky="ns")
            self.tree.configure(yscrollcommand=scrollbar.set)
        except Exception:
            # fallback a la scrollbar clásica de ttk si CTkScrollbar no está disponible
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            # ---- SCROLLBAR (fila 1, otra columna) ----
            scrollbar.grid(row=1, column=1, sticky="ns")
            self.tree.configure(yscrollcommand=scrollbar.set)

        # ============================================================
        #  ÁREA DE INTERACCIÓN (botones)
        # ============================================================

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=1, padx=10, pady=(15, 0), sticky="nsew")
        btn_frame.grid_rowconfigure((0,1,2,3), weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)

        interaccion_title = ctk.CTkLabel(btn_frame, text="Área de Interacción", font=self.fuente_subtitulo)
        interaccion_title.grid(row=0, column=0, sticky="n", pady=(0, 10))

        btn_style = {
            "width": 140,
            "height": 40,
            "fg_color": "#825c46",
            "hover_color": "#644736",
            "text_color": "white",
            "corner_radius": 10,
            "font": self.fuente_normal
        }

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_cliente, **btn_style).grid(row=1, column=0, padx = 10, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.confirmar_actualizacion_popup, **btn_style).grid(row=2, column=0, padx = 10, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.confirmar_eliminacion_popup, **btn_style).grid(row=3, column=0, padx = 10, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.mostrar_clientes, **btn_style).grid(row=4, column=0, padx = 10, pady=10, sticky="nsew")

        # ============================================================
        #  ÁREA DE CAMPOS
        # ============================================================

        form = ctk.CTkFrame(self)
        form.grid(row=2, column=0, columnspan=2, pady=(20,10), padx=10, sticky="nsew")
        for i in range(2):
            form.grid_columnconfigure(i, weight=1)
        
        campos_title = ctk.CTkLabel(form, text="Área de Campos", font=self.fuente_subtitulo)
        campos_title.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        # Campos del formulario (Entry cortos + Textarea para dirección)
        self.nombre = ctk.CTkEntry(form, placeholder_text="Nombre", font=self.fuente_normal)
        self.nombre.grid(row=1, column=0, padx=15, pady=15, sticky="ew")

        self.telefono = ctk.CTkEntry(form, placeholder_text="Teléfono", font=self.fuente_normal)
        self.telefono.grid(row=1, column=1, padx=15, pady=15, sticky="ew")

        self.correo = ctk.CTkEntry(form, placeholder_text="Correo", font=self.fuente_normal)
        self.correo.grid(row=2, column=0, padx=15, pady=15, sticky="ew")

        # textbox para dirección (intentar usar CTkTextbox si existe)
        try:
            self.direccion = ctk.CTkTextbox(form, width=1, height=80)
            self.direccion.configure(font=self.fuente_normal)
            self.direccion.grid(row=2, column=1, padx=15, pady=15, sticky="ew")

            # --- Placeholder ---
            self.direccion_placeholder = "Dirección"
            self.direccion.insert("1.0", self.direccion_placeholder)
            self.direccion.configure(text_color="#8a8a8a")  # gris suave

            def clear_placeholder(event):
                if self.direccion.get("1.0", "end-1c") == self.direccion_placeholder:
                    self.direccion.delete("1.0", "end")
                    self.direccion.configure(text_color="white")

            def restore_placeholder(event):
                if self.direccion.get("1.0", "end-1c").strip() == "":
                    self.direccion.insert("1.0", self.direccion_placeholder)
                    self.direccion.configure(text_color="#8a8a8a")

            self.direccion.bind("<FocusIn>", clear_placeholder)
            self.direccion.bind("<FocusOut>", restore_placeholder)

        except Exception:
            self.direccion = tk.Text(form, height=4, wrap="word", font=("Segoe UI", 12))
            self.direccion.grid(row=2, column=1, padx=5, pady=15, sticky="ew")

        # campo oculto id seleccionado
        self.id_seleccionado = None

        # enlazar selección de tabla
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # cargar inicialmente
        self.mostrar_clientes()
        self.after(200, self.ajustar_sidebar)
    
    # Ajuste automático del sidebar
    def ajustar_sidebar(self):
        altura_real = self.winfo_height() - 120

        if altura_real < 100:
            self.after(100, self.ajustar_sidebar)
            return

        self.sidebar.configure(height=altura_real)



    # -------------------------
    # helpers / util
    # -------------------------
    def _truncate(self, text, length=60):
        if not text:
            return ""
        t = str(text)
        return (t if len(t) <= length else t[:length-3] + "...")

    def popup(self, titulo, mensaje):
        win = ctk.CTkToplevel(self)
        win.title(titulo)
        win.geometry("360x160")
        win.resizable(False, False)
        win.grab_set()
        ctk.CTkLabel(win, text=mensaje, font=self.fuente_popup).pack(pady=16)
        ctk.CTkButton(win, text="Cerrar", fg_color="#825c46", hover_color="#644736", command=win.destroy, font=self.fuente_normal).pack(pady=10)

    # -------------------------
    # VALIDACIONES
    # -------------------------
    def validar_campos(self):
        if not self.nombre.get().strip():
            return "El campo NOMBRE está vacío."
        # teléfono y correo opcionales pero limpiar espacios
        return None

    # -------------------------
    # CRUD real usando src/crud/crud_cliente.py
    # -------------------------
    def mostrar_clientes(self):
        # limpiar
        for r in self.tree.get_children():
            self.tree.delete(r)

        try:
            clientes = obtener_clientes()
        except Exception as e:
            print("Error obtener_clientes:", e)
            clientes = []

        for c in clientes:
            direccion = c.get("direccion_cliente") or ""
            self.tree.insert("", "end", values=(
                c.get("id_cliente"),
                c.get("nombre_cliente"),
                c.get("telefono_cliente"),
                c.get("correo_cliente"),
                self._truncate(direccion, 60)
            ))

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        id_cliente = item["values"][0]
        # obtener datos completos
        cliente = obtener_cliente_por_id(id_cliente)
        if not cliente:
            return

        self.id_seleccionado = id_cliente
        self.nombre.delete(0, "end")
        self.nombre.insert(0, cliente.get("nombre_cliente", "") or "")

        self.telefono.delete(0, "end")
        self.telefono.insert(0, cliente.get("telefono_cliente", "") or "")

        self.correo.delete(0, "end")
        self.correo.insert(0, cliente.get("correo_cliente", "") or "")

        direccion = cliente.get("direccion_cliente", "") or ""
        try:
            # CTkTextbox
            self.direccion.delete("0.0", "end")
            self.direccion.insert("0.0", direccion)
        except Exception:
            # tk.Text
            self.direccion.delete("1.0", "end")
            self.direccion.insert("1.0", direccion)

    def crear_cliente(self):
        error = self.validar_campos()
        if error:
            self.popup("Error", error)
            return

        nombre = self.nombre.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        try:
            direccion = self.direccion.get("0.0", "end").strip()
        except Exception:
            direccion = self.direccion.get("1.0", "end").strip()

        ok = crear_cliente(nombre, telefono, correo, direccion)
        if ok:
            self.popup("Éxito", "Cliente creado correctamente.")
            self.mostrar_clientes()
        else:
            self.popup("Error", "No se pudo crear el cliente.")

    def confirmar_actualizacion_popup(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un cliente primero.")
            return

        error = self.validar_campos()
        if error:
            self.popup("Error", error)
            return

        nombre = self.nombre.get().strip() or "(sin nombre)"
        win = ctk.CTkToplevel(self)
        win.title("Confirmar actualización")
        win.geometry("380x170")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text=f"¿Estás seguro de actualizar ID: {self.id_seleccionado}\nNombre: {nombre}?", font=self.fuente_popup).pack(pady=16)

        ctk.CTkButton(win, text="Confirmar", fg_color="#825c46", hover_color="#644736",
                      command=lambda: [self._do_update_and_close(win)], font=self.fuente_normal).pack(pady=6)
        ctk.CTkButton(win, text="Cancelar", fg_color="#333", hover_color="#222", command=win.destroy, font=self.fuente_normal).pack(pady=4)

    def _do_update_and_close(self, win):
        self.actualizar_cliente()
        win.destroy()

    def actualizar_cliente(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un cliente primero.")
            return

        error = self.validar_campos()
        if error:
            self.popup("Error", error)
            return

        nombre = self.nombre.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        try:
            direccion = self.direccion.get("0.0", "end").strip()
        except Exception:
            direccion = self.direccion.get("1.0", "end").strip()

        ok = actualizar_cliente(self.id_seleccionado, nombre, telefono, correo, direccion)
        if ok:
            self.popup("Éxito", "Cliente actualizado correctamente.")
            self.mostrar_clientes()
        else:
            self.popup("Error", "No se pudo actualizar el cliente.")

    def confirmar_eliminacion_popup(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un cliente primero.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Confirmar eliminación")
        win.geometry("360x160")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text="¿Eliminar el cliente seleccionado?", font=self.fuente_popup).pack(pady=16)
        ctk.CTkButton(win, text="Sí, eliminar", fg_color="#8b0000", hover_color="#5a0000",
                      command=lambda: [self._do_delete_and_close(win)], font=self.fuente_normal).pack(pady=6)
        ctk.CTkButton(win, text="Cancelar", fg_color="#333", hover_color="#222", command=win.destroy, font=self.fuente_normal).pack(pady=4)

    def _do_delete_and_close(self, win):
        self.eliminar_cliente_confirmado()
        win.destroy()

    def eliminar_cliente_confirmado(self):
        if not self.id_seleccionado:
            self.popup("Error", "Selecciona un cliente primero.")
            return

        ok = eliminar_cliente(self.id_seleccionado)
        if ok:
            self.popup("Éxito", "Cliente eliminado.")
            self.mostrar_clientes()
            self.id_seleccionado = None
            # limpiar campos
            self.nombre.delete(0, "end")
            self.telefono.delete(0, "end")
            self.correo.delete(0, "end")
            try:
                self.direccion.delete("0.0", "end")
            except Exception:
                self.direccion.delete("1.0", "end")
        else:
            self.popup("Error", "No se pudo eliminar el cliente.")

    # ============================================================
    #  SIDEBAR OVERLAY (slide con place)
    # ============================================================
    def toggle_sidebar(self):
        if self.sidebar_visible:
            # Ocultar (slide hacia la izquierda)
            for x in range(0, 301, 5):
                self.sidebar.place(x=0 - x, y=120)
                self.sidebar.update()
            self.sidebar_visible = False
        else:
            # Mostrar (slide hacia la derecha)
            self.sidebar.lift()
            for x in range(-300, 1, 5):
                self.sidebar.place(x=x, y=120)
                self.sidebar.update()
            self.sidebar_visible = True
