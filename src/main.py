import customtkinter as ctk
from ui.ui_productos import ProductosUI
from ui.ui_empleados import EmpleadosUI
from ui.ui_clientes import ClientesUI
from ui.ui_proveedor import ProveedoresUI
from ui.ui_compra import ComprasUI
from ui.ui_venta import VentasUI

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Uniformes Bambi - Administración")
app.geometry("1280x720")

#ProductosUI(app)
#EmpleadosUI(app)
#ClientesUI(app)
#ProveedoresUI(app)
ComprasUI(app)
#VentasUI(app)

app.mainloop()

