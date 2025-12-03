import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class InicioUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # Fuentes compartidas
        self.fuente_titulo = ctk.CTkFont("Bell MT", 42, "bold")
        self.fuente_subtitulo = ctk.CTkFont("Bell MT", 25, "bold")
        self.fuente_normal = ctk.CTkFont("Segoe UI", 15)
        self.fuente_menu = ctk.CTkFont("Sitka", 17, "bold")

        self.grid(row=0, column=0, sticky="nsew")

        # ===================== SIDEBAR =========================
        self.sidebar_visible = False

        self.sidebar = ctk.CTkFrame(
            self,
            width=300,
            fg_color="#825c46"
        )
        self.sidebar.place(x=-300, y=120)
        self.after(200, self.ajustar_sidebar)
        self.sidebar.lift()

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



        # Botón de hamburguesa
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

        # Layout principal
        self.grid_rowconfigure(0, weight=0)  # botón hamburguesa
        self.grid_rowconfigure(1, weight=0)  # contenido
        self.grid_columnconfigure(0, weight=1)

        # ===================== CONTENIDO CENTRAL =========================

        contenedor = ctk.CTkFrame(self, fg_color="transparent")
        contenedor.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        contenedor.grid_rowconfigure(3, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        frame_titulo = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_titulo.grid(row=0, column=0, pady=(20, 5))

        emoji = ctk.CTkLabel(
            frame_titulo,
            text="🧵",
            font=("Segoe UI Emoji", 38)
        )
        emoji.pack(side="left", padx=20, pady=4)

        titulo = ctk.CTkLabel(
            frame_titulo,
            text="Bienvenido a 'Uniformes Bambi'",
            font=self.fuente_titulo
        )
        titulo.pack(side="left")

        emoji2 = ctk.CTkLabel(
            frame_titulo,
            text="📒",
            font=("Segoe UI Emoji", 38)
        )
        emoji2.pack(side="left", padx=20, pady=4)

        subt = ctk.CTkLabel(
            contenedor,
            text="Panel administrativo general",
            font=self.fuente_subtitulo
        )
        subt.grid(row=1, column=0, pady=(0, 30))

        # Panel decorativo central
        panel = ctk.CTkFrame(contenedor, corner_radius=20, fg_color="#fff6f0")
        panel.grid(row=2, column=0, padx=80, pady=20, sticky="nsew")
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        mensaje = ctk.CTkLabel(
            panel,
            text=(
                "Desde este sistema podrás gestionar productos, empleados, "
                "compras, ventas y clientes.\n\n"
                "Utiliza el menú lateral para navegar entre los módulos.\n"
            ),
            font=self.fuente_normal,
            text_color="#4a3f35",
            justify="center"
        )
        mensaje.pack(pady=40)

        # ===================== TARJETAS DE FUNCIONES ==========================

        cards_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        cards_frame.grid(row=3, column=0, pady=20, sticky="nsew")
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Cada tarjeta es un CTkFrame con un pequeño relieve
        def crear_card(parent, titulo, descripcion):
            card = ctk.CTkFrame(parent, corner_radius=5, fg_color="#fff", border_color="#c7b09a", border_width=2)
            card.grid_propagate(False)
            card.configure(width=360, height=200)

            ctk.CTkLabel(card, text=titulo, font=self.fuente_subtitulo).pack(pady=(10, 5))
            ctk.CTkLabel(card, text=descripcion, font=self.fuente_normal, justify="center", wraplength=300).pack(pady=(0, 10))
            return card
        
        crear_card(cards_frame, "Gestión de Productos", "Consulta, agrega y controla el inventario.").grid(row=0, column=0, padx=10, sticky="nsew")
        crear_card(cards_frame, "Empleados", "Administra personal, puestos y roles.").grid(row=0, column=1, padx=10, sticky="nsew")
        crear_card(cards_frame, "Ventas / Compras", "Control total de transacciones del negocio.").grid(row=0, column=2, padx=10,sticky="nsew")

    # ============================================
    # Ajuste automático del sidebar
    # ============================================
    def ajustar_sidebar(self):
        altura = self.winfo_height() - 120
        if altura < 120:
            self.after(100, self.ajustar_sidebar)
            return
        self.sidebar.configure(height=altura)

    # ============================================
    # Animación sidebar
    # ============================================
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
