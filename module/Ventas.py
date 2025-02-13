import json
from datetime import datetime  # Importa el módulo datetime
from module.Productos import Producto  # Importa la clase Producto

class Venta:
    def __init__(self, fecha,cliente, productos):
        self.fecha = fecha or datetime.now().isoformat()  # Fecha actual por defecto
        self.cliente = cliente
        self.productos = productos  # Lista de IDs de productos vendidos

    def calcular_total(self, productos_dict):
        total = 0
        for producto_id in self.productos:
            producto = productos_dict.get(producto_id)
            if producto:
                total += producto.precio
        return total

class GestionVentas:
    def __init__(self, nombre_archivo='data/ventas.json'): #ruta relativa a la carpeta datadef __init__(self, nombre_archivo='data/ventas.json'): #ruta relativa a la carpeta data
        self.nombre_archivo = nombre_archivo
        self.ventas = self.cargar_datos()
        if not isinstance(self.ventas, list): #verifica si self.ventas es una lista
            self.ventas = [] # si no lo es inicializala como una lista

    def cargar_datos(self):
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []  # Devuelve una lista vacía si el archivo no existe

    def guardar_datos(self):
        with open(self.nombre_archivo, 'w') as archivo:
            json.dump(self.ventas, archivo, indent=4)

    def registrar_venta(self, fecha,cliente, productos_ids, productos_dict):
        nueva_venta = Venta(fecha,cliente, productos_ids)
        self.ventas.append(nueva_venta.__dict__)  # Guarda el diccionario de la venta
        self.guardar_datos()
        # Actualizar el stock de los productos vendidos
        for producto_id in productos_ids:
            producto_data = productos_dict.get(producto_id)  # Obtén los datos del producto (diccionario)
            if producto_data:
                producto = Producto(producto_id, producto_data['nombre'], producto_data['stock'], producto_data['precio']) # Crea el objeto Producto
                producto.stock -= 1
                productos_dict[producto_id] = producto.__dict__ # Actualiza el diccionario con el objeto producto modificado
        return nueva_venta