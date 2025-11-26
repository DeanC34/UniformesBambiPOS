import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

# Importar CRUD de Proveedores
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
            fg_color="#21416B"
        )

        self.sidebar.place(
            x=-300,
            y=120,
            relheight=1
        )

        self.sidebar.lift()
        self.sidebar.grid(row=0, column=0, rowspan=50, sticky="nsw")
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
            ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                hover_color="#142944",
                text_color="white",
                font=self.fuente_menu,
                corner_radius=0,
                height=45,
                anchor="w"
            ).pack(fill="x", pady=2, padx=8)

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

        # Ajuste layout general
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=5)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        # ---------- TÍTULO PRINCIPAL ----------
        title = ctk.CTkLabel(self, text="Gestión de Proveedores", font=self.fuente_titulo)
        title.grid(row=1, column=0, columnspan=2, pady=20, sticky="n")

        # ---------- ESTILO TABLA ----------
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

        # ---- TABLA ----
        self.tabla_frame = ctk.CTkFrame(self)
        self.tabla_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)

        self.tabla_frame.grid_rowconfigure(0, weight=1)
        self.tabla_frame.grid_columnconfigure(0, weight=1)
        self.tabla_frame.grid_columnconfigure(1, weight=0)

        self.tree = ttk.Treeview(
            self.tabla_frame,
            columns=("ID", "Nombre", "Teléfono", "Correo", "Dirección"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Dirección", text="Dirección")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nombre", width=200)
        self.tree.column("Teléfono", width=140, anchor="center")
        self.tree.column("Correo", width=200)
        self.tree.column("Dirección", width=280)

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        try:
            scrollbar = ctk.CTkScrollbar(
                self.tabla_frame,
                command=self.tree.yview,
                width=14,
                fg_color="#1a1a1a",
                button_color="#21416B",
                button_hover_color="#142944"
            )
            scrollbar.grid(row=0, column=1, sticky="ns")
            self.tree.configure(yscrollcommand=scrollbar.set)
        except Exception:
            scrollbar = ttk.Scrollbar(self.tabla_frame, orient="vertical", command=self.tree.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            self.tree.configure(yscrollcommand=scrollbar.set)

        # ============================================================
        #  ÁREA DE INTERACCIÓN
        # ============================================================
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=2, column=1, padx=10, pady=(40, 0), sticky="nsew")
        btn_frame.grid_rowconfigure((0,1,2,3), weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(btn_frame, text="Área de Interacción", font=self.fuente_subtitulo).grid(
            row=0, column=0, sticky="n", pady=(0, 10)
        )

        btn_style = {
            "width": 140,
            "height": 40,
            "fg_color": "#21416B",
            "hover_color": "#142944",
            "text_color": "white",
            "corner_radius": 10,
            "font": self.fuente_normal
        }

        ctk.CTkButton(btn_frame, text="Crear", command=self.crear_proveedor, **btn_style).grid(row=1, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Actualizar", command=self.confirmar_actualizacion_popup, **btn_style).grid(row=2, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.confirmar_eliminacion_popup, **btn_style).grid(row=3, column=0, pady=10, sticky="nsew")
        ctk.CTkButton(btn_frame, text="Refrescar", command=self.mostrar_proveedores, **btn_style).grid(row=4, column=0, pady=10, sticky="nsew")

        # ============================================================
        #  FORMULARIO
        # ============================================================
        form = ctk.CTkFrame(self)
        form.grid(row=3, column=0, columnspan=2, pady=(20,10), padx=10, sticky="nsew")

        for i in range(2):
            form.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(form, text="Área de Campos", font=self.fuente_subtitulo).grid(
            row=0, column=0, columnspan=2, pady=(10, 0)
        )

        self.nombre = ctk.CTkEntry(form, placeholder_text="Nombre", font=self.fuente_normal)
        self.nombre.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.telefono = ctk.CTkEntry(form, placeholder_text="Teléfono", font=self.fuente_normal)
        self.telefono.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.correo = ctk.CTkEntry(form, placeholder_text="Correo", font=self.fuente_normal)
        self.correo.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # TEXTBOX DIRECCIÓN
        try:
            self.direccion = ctk.CTkTextbox(form, height=80, font=self.fuente_normal)
            self.direccion.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

            self.direccion_placeholder = "Dirección"
            self.direccion.insert("1.0", self.direccion_placeholder)
            self.direccion.configure(text_color="#8a8a8a")

            def clear_ph(event):
                if self.direccion.get("1.0", "end-1c") == self.direccion_placeholder:
                    self.direccion.delete("1.0", "end")
                    self.direccion.configure(text_color="white")

            def restore_ph(event):
                if self.direccion.get("1.0", "end-1c").strip() == "":
                    self.direccion.insert("1.0", self.direccion_placeholder)
                    self.direccion.configure(text_color="#8a8a8a")

            self.direccion.bind("<FocusIn>", clear_ph)
            self.direccion.bind("<FocusOut>", restore_ph)

        except Exception:
            self.direccion = tk.Text(form, height=4)
            self.direccion.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Seleccion
        self.id_seleccionado = None
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Cargar datos iniciales
        self.mostrar_proveedores()

    # ============================================================
    # UTIL
    # ============================================================
    def _truncate(self, text, length=60):
        return text if text and len(text) <= length else (text[:length-3] + "..." if text else "")

    def popup(self, titulo, msg):
        win = ctk.CTkToplevel(self)
        win.title(titulo)
        win.geometry("360x170")
        win.resizable(False, False)
        win.grab_set()
        ctk.CTkLabel(win, text=msg, font=self.fuente_popup).pack(pady=16)
        ctk.CTkButton(win, text="Cerrar", fg_color="#21416B", hover_color="#142944", command=win.destroy).pack(pady=6)

    # ============================================================
    # CRUD
    # ============================================================
    def mostrar_proveedores(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        proveedores = obtener_proveedores()

        for p in proveedores:
            self.tree.insert(
                "",
                "end",
                values=(
                    p["id_proveedor"],
                    p["nombre_proveedor"],
                    p["telefono_proveedor"],
                    p["correo_proveedor"],
                    self._truncate(p["direccion_proveedor"], 60)
                )
            )

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        item = self.tree.item(sel[0])
        id_proveedor = item["values"][0]
        proveedor = obtener_proveedor_por_id(id_proveedor)

        if not proveedor:
            return

        self.id_seleccionado = id_proveedor

        self.nombre.delete(0, "end")
        self.nombre.insert(0, proveedor.get("nombre_proveedor", ""))

        self.telefono.delete(0, "end")
        self.telefono.insert(0, proveedor.get("telefono_proveedor", ""))

        self.correo.delete(0, "end")
        self.correo.insert(0, proveedor.get("correo_proveedor", ""))

        direccion = proveedor.get("direccion_proveedor", "")

        try:
            self.direccion.delete("1.0", "end")
            self.direccion.insert("1.0", direccion)
            self.direccion.configure(text_color="white")
        except:
            self.direccion.delete("1.0", "end")
            self.direccion.insert("1.0", direccion)

    def crear_proveedor(self):
        if not self.nombre.get().strip():
            return self.popup("Error", "El campo NOMBRE está vacío.")

        nombre = self.nombre.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()

        try:
            direccion = self.direccion.get("1.0", "end").strip()
        except:
            direccion = ""

        if crear_proveedor(nombre, telefono, correo, direccion):
            self.popup("Éxito", "Proveedor creado correctamente.")
            self.mostrar_proveedores()
        else:
            self.popup("Error", "No se pudo crear el proveedor.")

    def confirmar_actualizacion_popup(self):
        if not self.id_seleccionado:
            return self.popup("Error", "Selecciona un proveedor primero.")

        win = ctk.CTkToplevel(self)
        win.title("Confirmar actualización")
        win.geometry("360x170")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text=f"¿Actualizar proveedor ID: {self.id_seleccionado}?", font=self.fuente_popup).pack(pady=16)

        ctk.CTkButton(
            win, text="Confirmar",
            fg_color="#21416B", hover_color="#142944",
            command=lambda: [self.actualizar_proveedor(), win.destroy()]
        ).pack(pady=6)

        ctk.CTkButton(win, text="Cancelar", fg_color="#333", hover_color="#222", command=win.destroy).pack(pady=4)

    def actualizar_proveedor(self):
        if not self.id_seleccionado:
            return self.popup("Error", "Selecciona un proveedor primero.")

        nombre = self.nombre.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()

        try:
            direccion = self.direccion.get("1.0", "end").strip()
        except:
            direccion = ""

        ok = actualizar_proveedor(self.id_seleccionado, nombre, telefono, correo, direccion)
        if ok:
            self.popup("Éxito", "Proveedor actualizado correctamente.")
            self.mostrar_proveedores()
        else:
            self.popup("Error", "No se pudo actualizar el proveedor.")

    def confirmar_eliminacion_popup(self):
        if not self.id_seleccionado:
            return self.popup("Error", "Selecciona un proveedor primero.")

        win = ctk.CTkToplevel(self)
        win.title("Confirmar eliminación")
        win.geometry("360x170")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text="¿Eliminar proveedor seleccionado?", font=self.fuente_popup).pack(pady=16)

        ctk.CTkButton(
            win, text="Eliminar",
            fg_color="#8b0000", hover_color="#5a0000",
            command=lambda: [self.eliminar_proveedor(), win.destroy()]
        ).pack(pady=6)

        ctk.CTkButton(win, text="Cancelar", fg_color="#333", hover_color="#222", command=win.destroy).pack(pady=4)

    def eliminar_proveedor(self):
        if eliminar_proveedor(self.id_seleccionado):
            self.popup("Éxito", "Proveedor eliminado.")
            self.mostrar_proveedores()
            self.id_seleccionado = None
        else:
            self.popup("Error", "No se pudo eliminar el proveedor.")

    # ============================================================
    # SIDEBAR ANIMACIÓN
    # ============================================================
    def toggle_sidebar(self):
        if self.sidebar_visible:
            for x in range(0, 301, 20):
                self.sidebar.place(x=0 - x, y=120)
                self.sidebar.update()
            self.sidebar_visible = False
        else:
            self.sidebar.lift()
            for x in range(-300, 1, 20):
                self.sidebar.place(x=x, y=120)
                self.sidebar.update()
            self.sidebar_visible = True
