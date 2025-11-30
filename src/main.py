import customtkinter as ctk
from ui.ui_productos import ProductosUI
from ui.ui_empleados import EmpleadosUI
from ui.ui_clientes import ClientesUI
from ui.ui_proveedor import ProveedoresUI
from ui.ui_compra import ComprasUI
from ui.ui_venta import VentasUI
import os

# Carpeta donde está main.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta completa al tema e icono
THEME_PATH = os.path.join(CURRENT_DIR, "ui", "coffee.json")

ICON_PATH = os.path.join(CURRENT_DIR, "ui", "bambi_icono.ico")  # pon tu archivo aquí


ctk.set_appearance_mode("light")
#ctk.set_default_color_theme("dark-blue")

ctk.set_default_color_theme(THEME_PATH)

app = ctk.CTk()
app.title("Uniformes Bambi - Administración")
app.geometry("1280x700")

# Cargar icono
try:
    app.iconbitmap(ICON_PATH)
except Exception as e:
    print("No se pudo cargar el icono:", e)

ProductosUI(app)
#EmpleadosUI(app)
#ClientesUI(app)
#ProveedoresUI(app)
#ComprasUI(app)
#VentasUI(app)

app.mainloop()

