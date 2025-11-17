import customtkinter as ctk
from crud.crud_producto import *

class ProductosUI(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="Gestión de Productos", font=("Arial", 18)).pack(pady=10)

        # Campos
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre del producto")
        self.nombre.pack(pady=5)

        self.descripcion = ctk.CTkEntry(self, placeholder_text="Descripción")
        self.descripcion.pack(pady=5)

        self.categoria = ctk.CTkOptionMenu(self, values=["escolar", "deportiva", "otra"])
        self.categoria.pack(pady=5)

        self.precio = ctk.CTkEntry(self, placeholder_text="Precio")
        self.precio.pack(pady=5)

        self.estado = ctk.CTkOptionMenu(self, values=["activo", "inactivo"])
        self.estado.pack(pady=5)

        # Botones
        ctk.CTkButton(self, text="Crear Producto", command=self.crear_producto).pack(pady=5)
        ctk.CTkButton(self, text="Mostrar Productos", command=self.mostrar_productos).pack(pady=5)

        # Tabla
        self.text_area = ctk.CTkTextbox(self, width=500, height=300)
        self.text_area.pack(pady=10)


    def crear_producto(self):
        ok = crear_producto(
            self.nombre.get(),
            self.descripcion.get(),
            self.categoria.get(),
            float(self.precio.get()),
            self.estado.get()
        )

        if ok:
            self.text_area.insert("end", "✔ Producto creado\n")
        else:
            self.text_area.insert("end", "❌ Error al crear producto\n")


    def mostrar_productos(self):
        data = obtener_productos()
        self.text_area.delete("1.0", "end")

        for p in data:
            self.text_area.insert(
                "end",
                f"{p['id_producto']} - {p['nombre_producto']} - {p['precio']}\n"
            )
