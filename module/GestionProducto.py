import json  # <--- Esta línea es la que falta
import os  # Importa el módulo os para trabajar con rutas

class GestionProductos:
    def __init__(self, nombre_archivo='data/productos.json'): #ruta relativa a la carpeta data
        
        self.nombre_archivo = nombre_archivo
        self.productos = self.cargar_datos()

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
        if id in self.productos:
            raise ValueError("Ya existe un producto con ese ID.")
        self.productos[id] = {'nombre': nombre, 'stock': stock, 'precio': precio}
        self.guardar_datos()

    def modificar_producto(self, id, nombre=None, stock=None, precio=None):
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