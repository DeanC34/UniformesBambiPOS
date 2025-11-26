import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from crud.crud_producto import *

class ProductosUI(ctk.CTkFrame):

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

        self.sidebar = ctk.CTkFrame(self, width=300, fg_color="#21416B")
        self.sidebar.place(x=-300, y=120, relheight=1)  # <-- empezamos oculto pero 60px abajo
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
            btn = ctk.CTkButton(
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
            btn.pack(fill="x", pady=2)

        # Botón para desplegar/cerrar menú
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

        # Layout general
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        # ---------- TÍTULO PRINCIPAL ----------
        title = ctk.CTkLabel(
            self,
            text="Gestión de Productos",
            font=self.fuente_titulo
        )
        title.grid(row=1, column=0, columnspan=2, pady=20, sticky="n")

        # ---------- ESTILO TABLA OSCURA ----------
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1a1a1a",
            foreground="white",
            rowheight=30,
            fieldbackground="#1a1a1a",
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

        # ---------- TABLA ----------
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Nombre", "Precio"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=0, sticky="nse")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # ============================================================
        #  ÁREA DE INTERACCIÓN
        # ============================================================
        self.interaccion_title = ctk.CTkLabel(
            self,
            text="Interacción básica",
            font=self.fuente_subtitulo
        )
        self.interaccion_title.grid(row=2, column=1, sticky="n", pady=(10, 0))

        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=2, column=1, padx=10, pady=(40, 0), sticky="nsew")
        btn_frame.grid_rowconfigure((0,1,2,3), weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)

        btn_style = {
            "width": 120,
            "height": 40,
            "fg_color": "#21416B",
            "hover_color": "#14273F",
            "text_color": "white",
            "corner_radius": 10,
            "font": self.fuente_normal
        }

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_producto, **btn_style).grid(row=0, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.confirmar_actualizacion_popup, **btn_style).grid(row=1, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_producto, **btn_style).grid(row=2, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.mostrar_productos, **btn_style).grid(row=3, column=0, pady=10, sticky="nsew")

        # ============================================================
        #  ÁREA DE CAMPOS
        # ============================================================
        self.campos_title = ctk.CTkLabel(
            self,
            text="Área de Campos",
            font=self.fuente_subtitulo
        )
        self.campos_title.grid(row=3, column=0, columnspan=2, sticky="n", pady=(10, 0))

        self.form = ctk.CTkFrame(self)
        self.form.grid(row=3, column=0, columnspan=2, pady=(40,10), padx=10, sticky="nsew")

        for i in range(2):
            self.form.grid_columnconfigure(i, weight=1)

        self.nombre = ctk.CTkEntry(self.form, placeholder_text="Nombre", font=self.fuente_normal)
        self.nombre.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.descripcion = ctk.CTkEntry(self.form, placeholder_text="Descripción", font=self.fuente_normal)
        self.descripcion.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.categoria = ctk.CTkOptionMenu(self.form, values=["escolar", "deportiva", "otra"], font=self.fuente_normal)
        self.categoria.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.precio = ctk.CTkEntry(self.form, placeholder_text="Precio", font=self.fuente_normal)
        self.precio.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.estado = ctk.CTkOptionMenu(self.form, values=["activo", "inactivo"], font=self.fuente_normal)
        self.estado.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.mostrar_productos()

    # ============================================================
    #  MÉTODOS CRUD REALES
    # ============================================================

    def mostrar_productos(self):
        self.tree.delete(*self.tree.get_children())
        productos = obtener_productos()

        for p in productos:
            self.tree.insert(
                "", "end",
                values=(p["id_producto"], p["nombre_producto"], p["precio"])
            )

        # Vincular selección una sola vez
        if not hasattr(self, "_tree_binded"):
            self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            self._tree_binded = True


    def on_tree_select(self, event):
        """Llena los campos al seleccionar una fila."""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        id_producto = item["values"][0]

        producto = obtener_producto_por_id(id_producto)
        if not producto:
            return

        self.id_seleccionado = id_producto
        self.nombre.delete(0, "end")
        self.nombre.insert(0, producto["nombre_producto"])

        self.descripcion.delete(0, "end")
        self.descripcion.insert(0, producto["descripcion_producto"])

        self.categoria.set(producto["categoria"])
        self.precio.delete(0, "end")
        self.precio.insert(0, str(producto["precio"]))

        self.estado.set(producto["estado"])


    def crear_producto(self):
        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        categoria = self.categoria.get()
        precio = self.precio.get()
        estado = self.estado.get()

        if not nombre or not precio:
            self.popup("Error", "El nombre y el precio son obligatorios.")
            return

        try:
            precio = float(precio)
        except:
            self.popup("Error", "El precio debe ser un número.")
            return

        ok = crear_producto(nombre, descripcion, categoria, precio, estado)

        if ok:
            self.popup("Éxito", "Producto creado correctamente.")
            self.mostrar_productos()
        else:
            self.popup("Error", "No se pudo crear el producto.")


    def confirmar_actualizacion_popup(self):
        if not hasattr(self, "id_seleccionado"):
            self.popup("Error", "Selecciona un producto primero.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Confirmar actualización")
        win.geometry("350x180")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="¿Actualizar este producto?", font=self.fuente_popup).pack(pady=20)

        ctk.CTkButton(win, text="Sí, actualizar", fg_color="#21416B",
                      hover_color="#14273F", command=lambda: [self.actualizar_producto(), win.destroy()]
                      ).pack(pady=5)

        ctk.CTkButton(win, text="Cancelar", fg_color="#333", hover_color="#222",
                      command=win.destroy).pack(pady=5)


    def actualizar_producto(self):
        idp = self.id_seleccionado
        nombre = self.nombre.get()
        descripcion = self.descripcion.get()
        categoria = self.categoria.get()
        precio = self.precio.get()
        estado = self.estado.get()

        if not nombre or not precio:
            self.popup("Error", "El nombre y precio son obligatorios.")
            return

        try:
            precio = float(precio)
        except:
            self.popup("Error", "El precio debe ser número.")
            return

        ok = actualizar_producto(idp, nombre, descripcion, categoria, precio, estado)

        if ok:
            self.popup("Éxito", "Producto actualizado.")
            self.mostrar_productos()
        else:
            self.popup("Error", "No se pudo actualizar.")


    def eliminar_producto(self):
        if not hasattr(self, "id_seleccionado"):
            self.popup("Error", "Selecciona un producto primero.")
            return

        win = ctk.CTkToplevel(self)
        win.title("Confirmar eliminación")
        win.geometry("350x180")
        win.resizable(False, False)

        ctk.CTkLabel(win, text="¿Eliminar el producto seleccionado?",
                     font=self.fuente_popup).pack(pady=20)

        ctk.CTkButton(win, text="Sí, eliminar", fg_color="#8b0000",
                      hover_color="#5a0000",
                      command=lambda: [self.eliminar_producto_confirmado(), win.destroy()]
                      ).pack(pady=5)

        ctk.CTkButton(win, text="Cancelar", fg_color="#333",
                      hover_color="#222", command=win.destroy).pack(pady=5)


    def eliminar_producto_confirmado(self):
        idp = self.id_seleccionado
        ok = eliminar_producto(idp)

        if ok:
            self.popup("Éxito", "Producto eliminado.")
            self.mostrar_productos()
        else:
            self.popup("Error", "No se pudo eliminar.")


    def popup(self, titulo, mensaje):
        win = ctk.CTkToplevel(self)
        win.title(titulo)
        win.geometry("350x170")
        win.resizable(False, False)

        ctk.CTkLabel(win, text=mensaje, font=self.fuente_popup).pack(pady=20)

        ctk.CTkButton(win, text="Cerrar", fg_color="#21416B",
                      hover_color="#14273F", command=win.destroy).pack(pady=10)

    # ============================================================
    #  SIDEBAR OVERLAY
    # ============================================================
    def toggle_sidebar(self):
        if self.sidebar_visible:
            # Ocultar (slide hacia la izquierda)
            for x in range(0, 301, 20):
                self.sidebar.place(x=0 - x, y=120)
                self.sidebar.update()
            self.sidebar_visible = False
        else:
            # Mostrar (slide hacia la derecha)
            self.sidebar.lift()
            for x in range(-300, 1, 20):
                self.sidebar.place(x=x, y=120)
                self.sidebar.update()
            self.sidebar_visible = True

