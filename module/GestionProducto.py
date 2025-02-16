import json  # <--- Esta línea es la que falta
import os  # Importa el módulo os para trabajar con rutas

class GestionProductos:
    def __init__(self, nombre_archivo='data/productos.json'): #ruta relativa a la carpeta data
        
        self.nombre_archivo = nombre_archivo
        self.productos = self.cargar_datos()

    def existe_producto(self, id_producto):
        return id_producto in self.productos  

    def cargar_datos(self):
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return {}

    def guardar_datos(self):
        with open(self.nombre_archivo, 'w') as archivo:
            json.dump(self.productos, archivo, indent=4)

    def agregar_producto(self, id, nombre, stock, precio):    
        id = id  

        # Validaciones
        if id in self.productos:
            raise ValueError("Ya existe un producto con ese ID.")
    
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock debe ser un número entero positivo.")

        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número positivo.")

    # Agregar el producto al diccionario con el ID dentro del producto
        self.productos[id] = {
        'id': id,
        'nombre': nombre,
        'stock': stock,
        'precio': precio
    }

    # Guardar cambios en el archivo JSON
        self.guardar_datos()
# Recargar la lista de productos desde el archivo JSON
        self.productos = self.cargar_datos()



    def editar_producto(self, id, nombre=None, stock=None, precio=None):
        if id not in self.productos:
            raise ValueError("No existe un producto con ese ID.")
        if nombre:
            self.productos[id]['nombre'] = nombre
        if stock:
            self.productos[id]['stock'] = stock
        if precio:
            self.productos[id]['precio'] = precio
        self.guardar_datos()

    def eliminar_producto(self, id):
        if id not in self.productos:
            raise ValueError("No existe un producto con ese ID.")
        del self.productos[id]
        self.guardar_datos()

    def obtener_todos(self):
        #print("🔹 Productos disponibles en obtener_todos():", self.productos)  # 🔹 Imprimir los 
        return self.productos
