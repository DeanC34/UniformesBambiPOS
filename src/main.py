import customtkinter as ctk
from ui.ui_productos import ProductosUI
from ui.ui_empleados import EmpleadosUI

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Uniformes Bambi - Administración")
app.geometry("900x600")

#ProductosUI(app)
EmpleadosUI(app)

app.mainloop()

