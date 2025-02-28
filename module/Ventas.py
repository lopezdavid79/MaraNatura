import json
import sys
import os
from datetime import datetime

class Venta:
    def __init__(self, id, fecha, cliente, productos):
        self.id = id
        self.fecha = fecha or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cliente = cliente
        self.productos = productos

class GestionVentas:
    def __init__(self, nombre_archivo_ventas='ventas.json', nombre_archivo_productos='data/productos.json'):
        self.nombre_archivo_ventas = nombre_archivo_ventas
        self.nombre_archivo_productos = nombre_archivo_productos
        self.ventas = self.cargar_datos(self.nombre_archivo_ventas)
        self.productos = self.cargar_datos(self.nombre_archivo_productos)
        self.id_counter = self.get_next_id()

    def _obtener_ruta_completa(self, nombre_archivo):
        """Obtiene la ruta completa al archivo JSON."""
        if getattr(sys, 'frozen', False):
            # Estamos en un paquete PyInstaller
            ruta_base = sys._MEIPASS
        else:
            # Estamos ejecutando desde el código fuente
            ruta_base = os.path.abspath('.')
        return os.path.join(ruta_base, 'data', nombre_archivo)

    def cargar_datos(self, nombre_archivo):
        """Carga los datos desde un archivo JSON."""
        ruta_completa = self._obtener_ruta_completa(nombre_archivo)
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Retorna una lista vacía en caso de error

    def guardar_datos(self):
        """Guarda los datos de ventas en el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa(self.nombre_archivo_ventas)
        try:
            with open(ruta_completa, 'w', encoding='utf-8') as archivo:
                json.dump(self.ventas, archivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar datos en {ruta_completa}: {e}")

    def get_next_id(self):
        """Obtiene el próximo ID disponible para una venta."""
        if not self.ventas:
            return 1
        return max(venta['id'] for venta in self.ventas) + 1

    def registrar_venta(self, fecha, cliente, productos_con_cantidad, productos_dict, total_venta):
        nuevo_id = len(self.ventas) + 1  # Asigna el siguiente ID disponible
        nueva_venta = Venta(nuevo_id, fecha, cliente, productos_con_cantidad)  # Pasa la lista de diccionarios

        # Guardar el total directamente en el diccionario de la venta
        venta_dict = nueva_venta.__dict__
        venta_dict["total"] = total_venta  # Guarda el total en el diccionario

        # Guarda el diccionario de la venta en la lista de ventas
        self.ventas.append(venta_dict)

        # Guardar los cambios de la venta en persistencia
        self.guardar_datos()

        # Actualizar stock
        self.actualizar_stock(productos_con_cantidad, productos_dict)  # Pasa la lista de diccionarios

        #print(f"Venta guardada: {venta_dict}")  # Imprime la venta registrada para debug
        return nueva_venta

    def actualizar_stock(self, productos_con_cantidad, productos_dict):
        """Actualiza el stock de los productos vendidos."""
        for producto_info in productos_con_cantidad:
            producto_id = producto_info["id_producto"]
            cantidad_vendida = producto_info["cantidad"]

            for producto_almacenado in productos_dict.values():
                if producto_almacenado["id"] == producto_id:
                    # Actualizar el stock
                    producto_almacenado["stock"] -= cantidad_vendida
                    print(f"Stock actualizado para producto ID {producto_id}: Nuevo stock = {producto_almacenado['stock']}")
                    # Guardar los cambios en el archivo JSON
                    self.guardar_productos(productos_dict)
                    break # Para evitar seguir iterando si ya se encontró el producto
            else: # Se ejecuta si el for termina sin un break.
                print(f"⚠️ Error: Producto con ID {producto_id} no encontrado en productos_dict.")        

    def guardar_productos(self, productos_dict):
            """Guarda los productos en el archivo JSON."""
            ruta_completa = self._obtener_ruta_completa("productos.json") # Se obtiene la ruta del archivo.
            try:
                with open(ruta_completa, 'w', encoding='utf-8') as archivo:
                    json.dump(productos_dict, archivo, indent=4, ensure_ascii=False)
                print("Stock actualizado y guardado correctamente.")
            except Exception as e:
                print(f"Error al guardar productos: {e}")

    def obtener_todos(self):
        return {str(index + 1): venta for index, venta in enumerate(self.ventas)}
