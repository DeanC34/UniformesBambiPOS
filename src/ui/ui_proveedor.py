import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# CRUD
from crud.crud_proveedor import (
    obtener_proveedores,
    crear_proveedor,
    obtener_proveedor_por_id,
    actualizar_proveedor,
    eliminar_proveedor
)


class ProveedoresUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # ---------- FUENTES ----------
        self.fuente_titulo = ctk.CTkFont("Segoe UI", 26, "bold")
        self.fuente_subtitulo = ctk.CTkFont("Segoe UI", 18, "bold")
        self.fuente_normal = ctk.CTkFont("Segoe UI", 14)
        self.fuente_popup = ctk.CTkFont("Segoe UI", 16)
        self.fuente_menu = ctk.CTkFont("Segoe UI", 15, "bold")

        self.grid(row=0, column=0, sticky="nsew")

        # ============================================================
        #   SIDEBAR DESPLEGABLE (MISMA LÓGICA QUE ProductosUI)
        # ============================================================
        self.sidebar_visible = False

        self.sidebar = ctk.CTkFrame(
            self,
            width=300,
            fg_color="#825c46"
        )

        self.sidebar.place(x=-300, y=120)
        self.sidebar.lift()

        menu_items = [
            "Inicio", "Productos", "Empleado", "Ventas", "Clientes",
            "Proveedores", "Compras", "Opciones", "Acerca de"
        ]

        for item in menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                hover_color="#644736",
                text_color="white",
                font=self.fuente_menu,
                corner_radius=0,
                height=45,
                anchor="w",
                command=lambda n=item: self.master.mostrar_pantalla(n)
            )
            btn.pack(fill="x", pady=2)

        # Botón toggle
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

        # ============================================================
        #               LAYOUT GENERAL (MISMO QUE PRODUCTOS)
        # ============================================================
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        # ---------- TÍTULO ----------
        title = ctk.CTkLabel(self, text="Gestión de Proveedores", font=self.fuente_titulo)
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # ============================================================
        #   ESTILO TABLA (CLONADO DE ProductosUI)
        # ============================================================
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#2c2517",
            foreground="white",
            rowheight=30,
            fieldbackground="#312b21",
            bordercolor="#333",
            borderwidth=1
        )
        style.configure(
            "Treeview.Heading",
            background="#333333",
            foreground="white",
            font=("Segoe UI", 12, "bold")
        )
        style.map("Treeview", background=[("selected", "#444")])

        # ============================================================
        #   TABLA PRINCIPAL (MISMA POSICIÓN Y LÓGICA)
        # ============================================================
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Nombre", "Teléfono", "Correo", "Dirección"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Dirección", text="Dirección")

        self.tree.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        scrollbar = ctk.CTkScrollbar(self, orientation="vertical")
        scrollbar.grid(row=1, column=0, sticky="nse")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # ============================================================
        #   ÁREA DE INTERACCIÓN (IGUAL A ProductosUI)
        # ============================================================
        self.interaccion_title = ctk.CTkLabel(
            self,
            text="Interacción básica",
            font=self.fuente_subtitulo
        )
        self.interaccion_title.grid(row=1, column=1, sticky="n", pady=(10, 0))

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=1, padx=10, pady=(40, 0), sticky="nsew")
        btn_frame.grid_rowconfigure((0,1,2,3), weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)

        btn_style = {
            "width": 120,
            "height": 40,
            "fg_color": "#825c46",
            "hover_color": "#644736",
            "text_color": "white",
            "corner_radius": 10,
            "font": self.fuente_normal
        }

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_proveedor, **btn_style).grid(row=0, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.confirmar_actualizacion_popup, **btn_style).grid(row=1, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.confirmar_eliminacion_popup, **btn_style).grid(row=2, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.mostrar_proveedores, **btn_style).grid(row=3, column=0, pady=10, sticky="nsew")

        # ============================================================
        #                     FORMULARIO
        # ============================================================
        self.campos_title = ctk.CTkLabel(
            self,
            text="Área de Campos",
            font=self.fuente_subtitulo
        )
        self.campos_title.grid(row=2, column=0, columnspan=2, sticky="n", pady=(10, 0))

        self.form = ctk.CTkFrame(self)
        self.form.grid(row=2, column=0, columnspan=2, pady=(40,10), padx=10, sticky="nsew")

        for i in range(2):
            self.form.grid_columnconfigure(i, weight=2)

        self.nombre = ctk.CTkEntry(self.form, placeholder_text="Nombre", font=self.fuente_normal)
        self.nombre.grid(row=0, column=0, padx=5, pady=15, sticky="ew")

        self.telefono = ctk.CTkEntry(self.form, placeholder_text="Teléfono", font=self.fuente_normal)
        self.telefono.grid(row=0, column=1, padx=5, pady=15, sticky="ew")

        self.correo = ctk.CTkEntry(self.form, placeholder_text="Correo", font=self.fuente_normal)
        self.correo.grid(row=1, column=0, padx=5, pady=15, sticky="ew")

        self.direccion = ctk.CTkEntry(self.form, placeholder_text="Dirección", font=self.fuente_normal)
        self.direccion.grid(row=1, column=1, padx=5, pady=15, sticky="ew")

        # ============================================================
        # INIT
        # ============================================================
        self.mostrar_proveedores()
        self.after(200, self.ajustar_sidebar)

    # Ajuste automático del sidebar
    def ajustar_sidebar(self):
        altura_real = self.winfo_height() - 120

        if altura_real < 100:
            self.after(100, self.ajustar_sidebar)
            return

        self.sidebar.configure(height=altura_real)

    # ============================================================
    # CRUD + POPUPS (DEJADOS TAL CUAL)
    # ============================================================

    def mostrar_proveedores(self):
        self.tree.delete(*self.tree.get_children())
        datos = obtener_proveedores()
        for p in datos:
            self.tree.insert("", "end",
                             values=(p["id_proveedor"], p["nombre"], p["telefono"], p["correo"], p["direccion"]))
        if not hasattr(self, "_binded"):
            self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            self._binded = True

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        idp = item["values"][0]
        prov = obtener_proveedor_por_id(idp)
        if not prov:
            return

        self.id_seleccionado = idp

        self.nombre.delete(0,"end")
        self.nombre.insert(0, prov["nombre"])

        self.telefono.delete(0,"end")
        self.telefono.insert(0, prov["telefono"])

        self.correo.delete(0,"end")
        self.correo.insert(0, prov["correo"])

        self.direccion.delete(0,"end")
        self.direccion.insert(0, prov["direccion"])

    # Crear
    def crear_proveedor(self):
        nombre = self.nombre.get()
        tel = self.telefono.get()
        correo = self.correo.get()
        dire = self.direccion.get()

        if not nombre:
            self.popup("Error", "El nombre es obligatorio.")
            return

        ok = crear_proveedor(nombre, tel, correo, dire)
        if ok:
            self.popup("Éxito", "Proveedor creado correctamente.")
            self.mostrar_proveedores()
        else:
            self.popup("Error", "No se pudo crear el proveedor.")

    # Popup actualizar
    def confirmar_actualizacion_popup(self):
        if not hasattr(self, "id_seleccionado"):
            self.popup("Error", "Selecciona un proveedor.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Actualizar")
        win.geometry("350x180")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="¿Actualizar proveedor?", font=self.fuente_popup).pack(pady=20)

        ctk.CTkButton(win, text="Sí, actualizar",
                      fg_color="#825c46",
                      hover_color="#644736",
                      command=lambda: [self.actualizar_proveedor(), win.destroy()]
                      ).pack(pady=5)

        ctk.CTkButton(win, text="Cancelar", fg_color="#333",
                      hover_color="#222",
                      command=win.destroy).pack(pady=5)

    def actualizar_proveedor(self):
        idp = self.id_seleccionado
        nombre = self.nombre.get()
        tel = self.telefono.get()
        correo = self.correo.get()
        dire = self.direccion.get()

        if not nombre:
            self.popup("Error", "El nombre es obligatorio.")
            return

        ok = actualizar_proveedor(idp, nombre, tel, correo, dire)
        if ok:
            self.popup("Éxito", "Proveedor actualizado.")
            self.mostrar_proveedores()
        else:
            self.popup("Error", "No se pudo actualizar.")

    # Popup eliminar
    def confirmar_eliminacion_popup(self):
        if not hasattr(self, "id_seleccionado"):
            self.popup("Error", "Selecciona un proveedor.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Eliminar")
        win.geometry("350x180")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="¿Eliminar proveedor?", font=self.fuente_popup).pack(pady=20)

        ctk.CTkButton(win, text="Sí, eliminar",
                      fg_color="#8b0000",
                      hover_color="#5a0000",
                      command=lambda: [self.eliminar_proveedor(), win.destroy()]
                      ).pack(pady=5)

        ctk.CTkButton(win, text="Cancelar", fg_color="#333",
                      hover_color="#222",
                      command=win.destroy).pack(pady=5)

    def eliminar_proveedor(self):
        ok = eliminar_proveedor(self.id_seleccionado)
        if ok:
            self.popup("Éxito", "Proveedor eliminado.")
            self.mostrar_proveedores()
        else:
            self.popup("Error", "No se pudo eliminar.")

    # Popup genérico
    def popup(self, titulo, mensaje):
        win = ctk.CTkToplevel(self)
        win.title(titulo)
        win.geometry("350x170")
        win.resizable(False, False)

        ctk.CTkLabel(win, text=mensaje, font=self.fuente_popup).pack(pady=20)

        ctk.CTkButton(win, text="Cerrar", fg_color="#825c46",
                      hover_color="#644736",
                      command=win.destroy).pack(pady=10)

    # ============================================================
    #   SIDE BAR TOGGLE
    # ============================================================
    def toggle_sidebar(self):
        if self.sidebar_visible:
            for x in range(0, 301, 5):
                self.sidebar.place(x=0 - x, y=120)
                self.sidebar.update()
            self.sidebar_visible = False
        else:
            self.sidebar.lift()
            for x in range(-300, 1, 5):
                self.sidebar.place(x=x, y=120)
                self.sidebar.update()
            self.sidebar_visible = True
