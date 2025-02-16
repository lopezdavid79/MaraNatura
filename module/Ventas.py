import json
from datetime import datetime  # Importa el módulo datetime
from module.Productos import Producto  # Importa la clase Producto

class Venta:
    def __init__(self, id, fecha,cliente, productos):
        self.id = id
        self.fecha = fecha or datetime.now().isoformat()  # Fecha actual por defecto
        self.cliente = cliente
        self.productos = productos  # Lis   ta de IDs de productos vendidos
        


    def calcular_total(self, productos_dict):

        
        #print(f"Diccionario recibido con {len(productos_dict)} elementos: {productos_dict}")
        total = 0
        for producto_id in self.productos:
            print(f"Tipo de producto_id: {type(producto_id)}")
        # Verificar si el producto_id existe en productos_dict
            if producto_id not in productos_dict:
                print(f"Advertencia: Producto con ID {producto_id} no encontrado en el diccionario.")
                continue  # Salta al siguiente producto si no se encuentra en el diccionario

            
            producto = productos_dict.get(producto_id)  # Obtén los datos del producto
        
            if producto:
                # Verifica que el producto tiene la clave "precio"
                if "precio" in producto:
                    precio_producto = producto["precio"]  # Accede al precio del producto
                    print(f"Producto ID: {producto_id}, Precio: {precio_producto}")  # Depuración: Verificar el precio
                    total += precio_producto  # Sumar el precio al total
                else:
                    print(f"Advertencia: El producto con ID {producto_id} no tiene la clave 'precio'.")
            else:
                print(f"Error: No se pudo obtener el producto con ID {producto_id}.")
    
        print(f"Total calculado: {total}")  # Depuración: Verificar el total calculado
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


    def registrar_venta(self, fecha, cliente, productos_ids, productos_dict, total_venta):
        nuevo_id = len(self.ventas) + 1  # Asigna el siguiente ID disponible
        nueva_venta = Venta(nuevo_id, fecha, cliente, productos_ids)

    # Guardar el total directamente en el diccionario de la venta
        venta_dict = nueva_venta.__dict__
        venta_dict["total"] = total_venta  # 🔹 Guarda el total en el diccionario
        self.ventas.append(venta_dict)  # Guarda el diccionario de la venta en la lista

        self.guardar_datos()  # Guardar cambios en persistencia

    # Actualizar el stock de los productos vendidos
        for producto_id in productos_ids:
            producto_data = productos_dict.get(producto_id)  # Obtén los datos del producto
            if producto_data:
                producto = Producto(producto_id, producto_data['nombre'], producto_data['stock'], producto_data['precio'])
                producto.stock -= 1
                productos_dict[producto_id] = producto.__dict__  # Actualiza el diccionario con el nuevo stock
        print(f"Venta guardada: {venta_dict}")
        return nueva_venta

    def obtener_todos(self):
        return {str(index + 1): venta for index, venta in enumerate(self.ventas)}
