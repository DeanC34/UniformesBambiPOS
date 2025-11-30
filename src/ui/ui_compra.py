import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from crud.crud_compra import *
from crud.crud_compradetalle import *

class ComprasUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        # validador de fechas
        self.register_validadores()

        # ---------- FUENTES ----------
        self.fuente_titulo = ctk.CTkFont("Segoe UI", 26, "bold")
        self.fuente_subtitulo = ctk.CTkFont("Segoe UI", 18, "bold")
        self.fuente_normal = ctk.CTkFont("Segoe UI", 14)
        self.fuente_menu = ctk.CTkFont("Segoe UI", 15, "bold")

        self.grid(row=0, column=0, sticky="nsew")


        # ---------- SIDEBAR ----------
        self._crear_sidebar()

        # ---------- GRID PRINCIPAL ----------
        self._configurar_layout()

        # ---------- TÍTULO ----------
        title = ctk.CTkLabel(self, text="Gestión de Compras", font=self.fuente_titulo)
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # ---------- TABLAS ----------
        self._crear_tabla_compras()
        self._crear_area_interaccion()
        self._crear_area_campos_compra()
        self._crear_tabla_detalles()
        self._crear_area_detalle_campos()

        # Carga inicial
        self.mostrar_compras()


    # =======================================================================
    # -------------------------- SIDEBAR -----------------------------------
    # =======================================================================
    def _crear_sidebar(self):
        self.sidebar_visible = False

        self.sidebar = ctk.CTkFrame(self, width=300, fg_color="#21416B")
        self.sidebar.place(x=-300, y=120, relheight=1)
        self.sidebar.grid(row=0, column=0, rowspan=50, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_remove()

        menu_items = [
            "Inicio", "Empleado", "Ventas",
            "Clientes", "Proveedores", "Compras",
            "Opciones", "Acerca de"
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


    # =======================================================================
    # ----------------------- LAYOUT PRINCIPAL ------------------------------
    # =======================================================================
    def _configurar_layout(self):
        self.grid_rowconfigure(0, weight=0) #altura boton_menu/titulo
        self.grid_rowconfigure(1, weight=1) # altura tablas
        self.grid_rowconfigure(2, weight=2) #altura campos
        self.grid_rowconfigure(3, weight=4) #altura segunda tabla

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)


    # =======================================================================
    # --------------------------- TABLA COMPRAS ------------------------------
    # =======================================================================
    def _crear_tabla_compras(self):

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1a1a1a",
            foreground="white",
            rowheight=20,
            fieldbackground="#1a1a1a"
        )
        style.configure(
            "Treeview.Heading",
            background="#333333",
            foreground="white",
            font=("Segoe UI", 12, "bold")
        )
        style.map("Treeview", background=[("selected", "#444")])

        self.frame_tabla_compras = ctk.CTkFrame(self)
        self.frame_tabla_compras.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        self.frame_tabla_compras.grid_rowconfigure(0, weight=1)
        self.frame_tabla_compras.grid_columnconfigure(0, weight=1)
        self.frame_tabla_compras.grid_columnconfigure(1, weight=0)

        self.tree_compras = ttk.Treeview(
            self.frame_tabla_compras,
            columns=("ID", "Fecha", "Total", "Proveedor"),
            show="headings"
        )
        self.tree_compras.heading("ID", text="ID")
        self.tree_compras.heading("Fecha", text="Fecha")
        self.tree_compras.heading("Total", text="Total")
        self.tree_compras.heading("Proveedor", text="Proveedor")

        self.tree_compras.column("ID", width=60, anchor="center")
        self.tree_compras.column("Fecha", width=150)
        self.tree_compras.column("Total", width=120)
        self.tree_compras.column("Proveedor", width=160)

        self.tree_compras.grid(row=0, column=0, sticky="nsew")

        try:
            scrollbar = ctk.CTkScrollbar(
                self.frame_tabla_compras,
                command=self.tree_compras.yview,
                width=14,
                fg_color="#1a1a1a",
                button_color="#21416B",
                button_hover_color="#142944"
            )
            scrollbar.grid(row=0, column=1, sticky="ns")
            self.tree_compras.configure(yscrollcommand=scrollbar.set)

        except Exception:
            scrollbar = ttk.Scrollbar(self.frame_tabla_compras, orient="vertical", command=self.tree_compras.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            self.tree_compras.configure(yscrollcommand=scrollbar.set)

        self.tree_compras.bind("<<TreeviewSelect>>", self.on_select_compra)


    # =======================================================================
    # ----------------------- BOTONES CRUD COMPRAS --------------------------
    # =======================================================================
    def _crear_area_interaccion(self):
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

        ctk.CTkLabel(btn_frame, text="Acciones", font=self.fuente_subtitulo)\
            .grid(row=0, column=0, pady=10)

        style = {
            "width": 140,
            "height": 40,
            "fg_color": "#21416B",
            "hover_color": "#142944",
            "text_color": "white",
            "corner_radius": 10,
            "font": self.fuente_normal
        }

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_compra, **style).grid(row=1, column=0, pady=5)
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.actualizar_compra, **style).grid(row=2, column=0, pady=5)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_compra, **style).grid(row=3, column=0, pady=5)
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.mostrar_compras, **style).grid(row=4, column=0, pady=5)


    # ======================================================================
    # --------------------------- CAMPOS COMPRA -----------------------------
    # ======================================================================
    def _crear_area_campos_compra(self):
        form = ctk.CTkFrame(self)
        form.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        form.grid_columnconfigure((0,1,2), weight=1)

        ctk.CTkLabel(form, text="Datos de la Compra", font=self.fuente_subtitulo)\
            .grid(row=0, column=0, columnspan=3, pady=10)

        self.fecha = ctk.CTkEntry(
            form,
            placeholder_text="Fecha (YYYY-MM-DD)",
            #validate="key",
            validatecommand=self.vcmd_fecha
        )

        self.fecha.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.total = ctk.CTkEntry(form, placeholder_text="Total")
        self.total.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.proveedor = ctk.CTkEntry(form, placeholder_text="ID Proveedor")
        self.proveedor.grid(row=2, column=2, padx=5, pady=5, sticky="ew")


    # ======================================================================
    # --------------------- TABLA DETALLES DE COMPRA -----------------------
    # ======================================================================
    def _crear_tabla_detalles(self):

        self.frame_detalles = ctk.CTkFrame(self)
        self.frame_detalles.grid(row=3, column=0, sticky="nsew", padx=15, pady=10)

        self.frame_detalles.grid_rowconfigure(0, weight=1)
        self.frame_detalles.grid_columnconfigure(0, weight=1)
        self.frame_detalles.grid_columnconfigure(1, weight=0)

        self.tree_detalle = ttk.Treeview(
            self.frame_detalles,
            columns=("ID", "Cantidad", "Precio", "Variación", "CompraID"),
            show="headings"
        )

        encabezados = [
            ("ID", "ID"),
            ("Cantidad", "Cantidad"),
            ("Precio", "Precio Unitario"),
            ("Variación", "ID Variación"),
            ("CompraID", "ID Compra")
        ]

        for col, titulo in encabezados:
            self.tree_detalle.heading(col, text=titulo)

        self.tree_detalle.column("ID", width=70, anchor="center")
        self.tree_detalle.column("Cantidad", width=120)
        self.tree_detalle.column("Precio", width=130)
        self.tree_detalle.column("Variación", width=130)
        self.tree_detalle.column("CompraID", width=120)

        self.tree_detalle.grid(row=0, column=0, sticky="nsew")

        try:
            scrollbar = ctk.CTkScrollbar(
                self.frame_detalles,
                command=self.tree_detalle.yview,
                width=14,
                fg_color="#1a1a1a",
                button_color="#21416B",
                button_hover_color="#142944"
            )
            scrollbar.grid(row=0, column=1, sticky="ns")
            self.tree_detalle.configure(yscrollcommand=scrollbar.set)

        except Exception:
            scrollbar = ttk.Scrollbar(self.frame_detalles, orient="vertical", command=self.tree_detalle.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            self.tree_detalle.configure(yscrollcommand=scrollbar.set)


    # ======================================================================
    # ---------------------- CAMPOS DETALLE COMPRA -------------------------
    # ======================================================================
    def _crear_area_detalle_campos(self):

        form = ctk.CTkFrame(self)
        form.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        form.grid_columnconfigure(0, weight=1)
        form.grid_rowconfigure((0,1,2,3,4,5), weight=1)

        ctk.CTkLabel(form, text="Detalles de Compra", font=self.fuente_subtitulo)\
            .grid(row=0, column=0, pady=10)

        self.det_cantidad = ctk.CTkEntry(form, placeholder_text="Cantidad")
        self.det_cantidad.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.det_precio = ctk.CTkEntry(form, placeholder_text="Precio Unitario")
        self.det_precio.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.det_variacion = ctk.CTkEntry(form, placeholder_text="ID Variación Producto")
        self.det_variacion.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # ⭐ Campo añadido (autollenado)
        self.det_compra = ctk.CTkEntry(form, placeholder_text="ID Compra (auto)")
        self.det_compra.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(form, text="Agregar Detalle", fg_color="#21416B",
                      command=self.ui_agregar_detalle)\
            .grid(row=5, column=0, pady=10, sticky="ew")


    # ======================================================================
    # ------------------------ CARGA DE DATOS -------------------------------
    # ======================================================================
    def mostrar_compras(self):
        for row in self.tree_compras.get_children():
            self.tree_compras.delete(row)

        compras = obtener_compras()
        for c in compras:
            self.tree_compras.insert("", "end", values=(
                c["id_compra"], c["fecha_compra"], c["total_compra"], c["Proveedor_id_proveedor"]
            ))

    def on_select_compra(self, event):
        sel = self.tree_compras.selection()
        if not sel:
            return
        item = self.tree_compras.item(sel[0])
        id_compra = item["values"][0]

        compra = obtener_compra_por_id(id_compra)
        if not compra:
            return

        # Mostrar datos
        self.fecha.delete(0, "end")
        self.fecha.insert(0, compra["fecha_compra"])

        self.total.delete(0, "end")
        self.total.insert(0, compra["total_compra"])

        self.proveedor.delete(0, "end")
        self.proveedor.insert(0, compra["Proveedor_id_proveedor"])

        # 👉 Autollenar ID de compra en el formulario de detalle
        self.det_compra.delete(0, "end")
        self.det_compra.insert(0, id_compra)

        # Cargar detalles
        self.mostrar_detalles(id_compra)

    def mostrar_detalles(self, id_compra):

        id_compra = int(id_compra)

        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)

        detalles = obtener_detalles_compra()
        for d in detalles:
            if int(d["Compra_id_compra"]) == id_compra:
                self.tree_detalle.insert("", "end", values=(
                    d["id_compra_detalle"],
                    d["cantidad"],
                    d["preciounitario"],
                    d["VariacionProducto_id_variacion"],
                    d["Compra_id_compra"]
                ))

    #Validador de fechas
    import datetime

    def register_validadores(self):
        vcmd = (self.register(self.validar_fecha_tecla), '%P')
        self.vcmd_fecha = vcmd


    def validar_fecha_tecla(self, texto):
        # Permite borrar todo
        if texto == "-":
            return True

        # Permite solo números y guiones
        for c in texto:
            if not (c.isdigit() or c == "-"):
                return False

        # Máximo 10 caracteres
        if len(texto) > 10:
            return False

        # Evita que escriban más de 4 dígitos al inicio
        if len(texto) >= 5:
            if texto[4] != "-":
                return False

        # Evita que escriban más de 2 dígitos en el mes
        if len(texto) >= 8:
            if texto[7] != "-":
                return False

        return True

    def validar_fecha_completa(self, fecha_texto):
        try:
            datetime.datetime.strptime(fecha_texto, "%Y-%m-%d")
            return True
        except ValueError:
            return False


    # ======================================================================
    # ---------------------------- CRUD COMPRA ------------------------------
    # ======================================================================
    def crear_compra(self):
        if not self.validar_fecha_completa(self.fecha.get()):
            messagebox.showerror("Fecha inválida", "Introduce una fecha válida con el formato YYYY-MM-DD.")
            return

        crear_compra(self.fecha.get(), self.total.get(), self.proveedor.get())
        self.mostrar_compras()

    def actualizar_compra(self):
        sel = self.tree_compras.selection()
        if not sel:
            return

        if not self.validar_fecha_completa(self.fecha.get()):
            messagebox.showerror("Fecha inválida", "Introduce una fecha válida con formato YYYY-MM-DD.")
            return

        id_compra = self.tree_compras.item(sel[0])["values"][0]
        actualizar_compra(id_compra, self.fecha.get(), self.total.get(), self.proveedor.get())
        self.mostrar_compras()

    def eliminar_compra(self):
        sel = self.tree_compras.selection()
        if not sel:
            return
        id_compra = self.tree_compras.item(sel[0])["values"][0]
        eliminar_compra(id_compra)
        self.mostrar_compras()

    # ======================================================================
    # ---------------------------- CRUD DETALLE -----------------------------
    # ======================================================================
    def ui_agregar_detalle(self):
        print(">>> ui_agregar_detalle() fue llamado")

        if self.det_compra.get().strip() == "":
            messagebox.showwarning(
                "Sin compra seleccionada",
                "Debes seleccionar una compra antes de agregar un detalle."
            )
            return

        try:
            cantidad = int(self.det_cantidad.get())
            precio = float(self.det_precio.get())
            variacion = int(self.det_variacion.get())
            compra = int(self.det_compra.get())  # ← ahora sí llega lleno
        except ValueError:
            print("❌ Error: uno de los valores no es numérico.")
            return

        crear_detalle_compra(cantidad, precio, variacion, compra)

        # Recarga TOTAL asegurando coherencia
        self.on_select_compra(None)

    # ======================================================================
    # ------------------------- SIDEBAR ANIMADO -----------------------------
    # ======================================================================
    def toggle_sidebar(self):
        if self.sidebar_visible:
            for x in range(0, 301, 20):
                self.sidebar.place(x=-x, y=120)
                self.sidebar.update()
            self.sidebar_visible = False
        else:
            self.sidebar.lift()
            for x in range(-300, 1, 20):
                self.sidebar.place(x=x, y=120)
                self.sidebar.update()
            self.sidebar_visible = True
