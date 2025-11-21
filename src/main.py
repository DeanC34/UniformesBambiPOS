import customtkinter as ctk
from ui.ui_productos import ProductosUI

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Uniformes Bambi - Administración")
app.geometry("900x600")

ProductosUI(app)

app.mainloop()

