import customtkinter as ctk
import os
# Importar todas las pantallas
from ui.ui_productos import ProductosUI
from ui.ui_empleados import EmpleadosUI
from ui.ui_clientes import ClientesUI
from ui.ui_proveedor import ProveedoresUI
from ui.ui_compra import ComprasUI
from ui.ui_venta import VentasUI
from ui.ui_inicio import InicioUI

# ================ CONFIGURACIÓN DE RUTAS ===================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(CURRENT_DIR, "ui", "coffee.json")
ICON_PATH = os.path.join(CURRENT_DIR, "ui", "bambi_icono.ico")

# Aplica tema **ANTES** de crear la ventana principal
ctk.set_appearance_mode("light")
ctk.set_default_color_theme(THEME_PATH)

# ================ APLICACIÓN PRINCIPAL ======================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Uniformes Bambi - Administración")
        self.geometry("1280x700")

        try:
            self.iconbitmap(ICON_PATH)
        except:
            print("No se pudo cargar el icono.")

        # 💡 ESTA ES LA PARTE QUE FALTABA 💡
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Tabla de pantallas disponibles
        self.pantallas = {
            "Inicio": InicioUI,
            "Productos": ProductosUI,
            "Empleado": EmpleadosUI,
            "Clientes": ClientesUI,
            "Proveedores": ProveedoresUI,
            "Compras": ComprasUI,
            "Ventas": VentasUI,
        }

        # Pantalla inicial
        self.current_frame = InicioUI(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")


    # ================= GESTOR DE PANTALLAS ===================
    def mostrar_pantalla(self, nombre):
        if nombre not in self.pantallas:
            print("Pantalla no registrada:", nombre)
            return

        # Quitar la pantalla actual
        self.current_frame.grid_forget()

        # Crear y mostrar la nueva
        FrameClass = self.pantallas[nombre]
        self.current_frame = FrameClass(self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

# ================ EJECUCIÓN ======================
if __name__ == "__main__":
    app = App()
    app.mainloop()
