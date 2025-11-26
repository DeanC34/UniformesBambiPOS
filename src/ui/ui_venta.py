import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from crud.crud_venta import *
from crud.crud_ventadetalle import *

class VentasUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # ---------- FUENTES ----------
        self.fuente_titulo = ctk.CTkFont("Segoe UI", 26, "bold")
        self.fuente_subtitulo = ctk.CTkFont("Segoe UI", 18, "bold")
        self.fuente_normal = ctk.CTkFont("Segoe UI", 14)
        self.fuente_menu = ctk.CTkFont("Segoe UI", 15, "bold")

        self.pack(fill="both", expand=True)

        self._crear_sidebar()
        self._configurar_layout()

        title = ctk.CTkLabel(self, text="Gestión de Ventas", font=self.fuente_titulo)
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        self._crear_tabla_ventas()
        self._crear_area_interaccion()
        self._crear_area_campos_venta()
        self._crear_tabla_detalles()
        self._crear_area_detalle_campos()

        self.mostrar_ventas()

    # ======================================================================
    # SIDEBAR
    # ======================================================================
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

    # ======================================================================
    # LAYOUT
    # ======================================================================
    def _configurar_layout(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=4)

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

    # ======================================================================
    # TABLA VENTAS
    # ======================================================================
    def _crear_tabla_ventas(self):

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

        self.frame_tabla_ventas = ctk.CTkFrame(self)
        self.frame_tabla_ventas.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        self.frame_tabla_ventas.grid_rowconfigure(0, weight=1)
        self.frame_tabla_ventas.grid_columnconfigure(0, weight=1)
        self.frame_tabla_ventas.grid_columnconfigure(1, weight=0)

        self.tree_ventas = ttk.Treeview(
            self.frame_tabla_ventas,
            columns=("ID", "Fecha", "Total", "Cliente"),
            show="headings"
        )
        self.tree_ventas.heading("ID", text="ID")
        self.tree_ventas.heading("Fecha", text="Fecha")
        self.tree_ventas.heading("Total", text="Total")
        self.tree_ventas.heading("Cliente", text="Cliente")

        self.tree_ventas.column("ID", width=60, anchor="center")
        self.tree_ventas.column("Fecha", width=150)
        self.tree_ventas.column("Total", width=120)
        self.tree_ventas.column("Cliente", width=160)

        self.tree_ventas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame_tabla_ventas, orient="vertical", command=self.tree_ventas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_ventas.configure(yscrollcommand=scrollbar.set)

        self.tree_ventas.bind("<<TreeviewSelect>>", self.on_select_venta)

    # ======================================================================
    # BOTONES CRUD
    # ======================================================================
    def _crear_area_interaccion(self):
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

        ctk.CTkLabel(btn_frame, text="Acciones", font=self.fuente_subtitulo).grid(row=0, column=0, pady=10)

        style = {
            "width": 140,
            "height": 40,
            "fg_color": "#21416B",
            "hover_color": "#142944",
            "text_color": "white",
            "corner_radius": 10,
            "font": self.fuente_normal
        }

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_venta, **style).grid(row=1, column=0, pady=5)
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.actualizar_venta, **style).grid(row=2, column=0, pady=5)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.eliminar_venta, **style).grid(row=3, column=0, pady=5)
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.mostrar_ventas, **style).grid(row=4, column=0, pady=5)

    # ======================================================================
    # FORMULARIO VENTA
    # ======================================================================
    def _crear_area_campos_venta(self):
        form = ctk.CTkFrame(self)
        form.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        form.grid_columnconfigure((0,1,2), weight=1)

        ctk.CTkLabel(form, text="Datos de la Venta", font=self.fuente_subtitulo).grid(row=0, column=0, columnspan=3, pady=10)

        self.fecha = ctk.CTkEntry(form, placeholder_text="Fecha (YYYY-MM-DD)")
        self.fecha.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.total = ctk.CTkEntry(form, placeholder_text="Total")
        self.total.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.cliente = ctk.CTkEntry(form, placeholder_text="ID Cliente")
        self.cliente.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

    # ======================================================================
    # TABLA DETALLE VENTA
    # ======================================================================
    def _crear_tabla_detalles(self):

        self.frame_detalles = ctk.CTkFrame(self)
        self.frame_detalles.grid(row=3, column=0, sticky="nsew", padx=15, pady=10)

        self.frame_detalles.grid_rowconfigure(0, weight=1)
        self.frame_detalles.grid_columnconfigure(0, weight=1)
        self.frame_detalles.grid_columnconfigure(1, weight=0)

        self.tree_detalle = ttk.Treeview(
            self.frame_detalles,
            columns=("ID", "Cantidad", "Precio", "Variación", "VentaID"),
            show="headings"
        )

        encabezados = [
            ("ID", "ID"),
            ("Cantidad", "Cantidad"),
            ("Precio", "Precio Unitario"),
            ("Variación", "ID Variación"),
            ("VentaID", "ID Venta")
        ]

        for col, titulo in encabezados:
            self.tree_detalle.heading(col, text=titulo)

        self.tree_detalle.column("ID", width=70, anchor="center")
        self.tree_detalle.column("Cantidad", width=120)
        self.tree_detalle.column("Precio", width=130)
        self.tree_detalle.column("Variación", width=130)
        self.tree_detalle.column("VentaID", width=120)

        self.tree_detalle.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame_detalles, orient="vertical", command=self.tree_detalle.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_detalle.configure(yscrollcommand=scrollbar.set)

    # ======================================================================
    # CAMPOS DETALLE
    # ======================================================================
    def _crear_area_detalle_campos(self):

        form = ctk.CTkFrame(self)
        form.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(form, text="Detalles de Venta", font=self.fuente_subtitulo)\
            .grid(row=0, column=0, pady=10)

        self.det_cantidad = ctk.CTkEntry(form, placeholder_text="Cantidad")
        self.det_cantidad.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.det_precio = ctk.CTkEntry(form, placeholder_text="Precio Unitario")
        self.det_precio.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.det_variacion = ctk.CTkEntry(form, placeholder_text="ID Variación Producto")
        self.det_variacion.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.det_venta = ctk.CTkEntry(form, placeholder_text="ID Venta (auto)")
        self.det_venta.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(
            form, text="Agregar Detalle", fg_color="#21416B",
            command=self.ui_agregar_detalle
        ).grid(row=5, column=0, pady=10, sticky="ew")

    # ======================================================================
    # CARGA DE DATOS
    # ======================================================================
    def mostrar_ventas(self):
        for row in self.tree_ventas.get_children():
            self.tree_ventas.delete(row)

        ventas = obtener_ventas()
        for v in ventas:
            self.tree_ventas.insert("", "end", values=(
                v["id_venta"], v["fecha_venta"],
                v["total_venta"], v["Cliente_id_cliente"]
            ))

    def on_select_venta(self, event):
        sel = self.tree_ventas.selection()
        if not sel:
            return

        item = self.tree_ventas.item(sel[0])
        id_venta = item["values"][0]

        venta = obtener_venta_por_id(id_venta)
        if not venta:
            return

        self.fecha.delete(0, "end")
        self.fecha.insert(0, venta["fecha_venta"])

        self.total.delete(0, "end")
        self.total.insert(0, venta["total_venta"])

        self.cliente.delete(0, "end")
        self.cliente.insert(0, venta["Cliente_id_cliente"])

        self.det_venta.delete(0, "end")
        self.det_venta.insert(0, id_venta)

        self.mostrar_detalles(id_venta)

    def mostrar_detalles(self, id_venta):

        id_venta = int(id_venta)

        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)

        detalles = obtener_detalles_venta()
        for d in detalles:
            if int(d["Venta_id_venta"]) == id_venta:
                self.tree_detalle.insert("", "end", values=(
                    d["id_detalle"],
                    d["cantidad"],
                    d["precio_unitario"],
                    d["VariacionProducto_id_variacion"],
                    d["Venta_id_venta"]
                ))

    # ======================================================================
    # CRUD VENTAS
    # ======================================================================
    def crear_venta(self):
        id_venta = crear_venta(self.fecha.get(), self.total.get(), self.cliente.get())
        self.mostrar_ventas()

    def actualizar_venta(self):
        sel = self.tree_ventas.selection()
        if not sel:
            return
        id_venta = self.tree_ventas.item(sel[0])["values"][0]
        actualizar_venta(id_venta, self.fecha.get(), self.total.get(), self.cliente.get())
        self.mostrar_ventas()

    def eliminar_venta(self):
        sel = self.tree_ventas.selection()
        if not sel:
            return
        id_venta = self.tree_ventas.item(sel[0])["values"][0]
        eliminar_venta(id_venta)
        self.mostrar_ventas()

    # ======================================================================
    # CRUD DETALLE
    # ======================================================================
    def ui_agregar_detalle(self):
        print(">>> ui_agregar_detalle_venta() fue llamado")

        if self.det_venta.get().strip() == "":
            messagebox.showwarning(
                "Sin venta seleccionada",
                "Debes seleccionar una venta antes de agregar un detalle."
            )
            return


        try:
            cantidad = int(self.det_cantidad.get())
            precio_unitario = float(self.det_precio.get())
            variacion = int(self.det_variacion.get())
            venta = int(self.det_venta.get())

        except ValueError:
            print("❌ Error: valores no numéricos.")
            return

        crear_detalle_venta(cantidad, precio_unitario, variacion, venta)

        self.on_select_venta(None)

    # ======================================================================
    # SIDEBAR ANIMADO
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
