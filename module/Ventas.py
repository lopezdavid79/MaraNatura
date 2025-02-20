import json
from datetime import datetime  # Importa el módulo datetime
from module.Productos import Producto  # Importa la clase Producto
from module.GestionProducto import GestionProductos
gestion_productos =GestionProductos()
class Venta:
    def __init__(self, id, fecha,cliente, productos):
        self.id = id
        self.fecha = fecha or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
        venta_dict["total"] = total_venta  # Guarda el total en el diccionario

        # Guarda el diccionario de la venta en la lista de ventas
        self.ventas.append(venta_dict)
        
        # Guardar los cambios de la venta en persistencia
        self.guardar_datos()

            # **Actualizar stock**
        self.actualizar_stock(productos_ids, productos_dict)

        #print(f"Venta guardada: {venta_dict}")  # Imprime la venta registrada para debug
        return nueva_venta

    def actualizar_stock(self, productos_ids, productos_dict):
        """Método separado para actualizar el stock de los productos vendidos."""
        print("\n🔍 [DEPURACIÓN] Estructura de productos_dict antes de actualizar:")
        print(json.dumps(productos_dict, indent=4, ensure_ascii=False))  # Imprime bien formateado
        for producto_id in productos_ids:
            producto_id_str = str(producto_id)  # Convertimos explícitamente a string
            print(f"\n🔎 Buscando producto ID: {producto_id} (tipo: {type(producto_id_str)})")
            producto_data = productos_dict.get(producto_id_str)  # Obtén los datos del producto
            print(producto_data)
                    
            if producto_data:
                        #Verificar si el stock es suficiente
                if producto_data['stock'] > 0:
                    producto_data['stock'] -= 1  # Restamos uno al stock
                    productos_dict[producto_id] = producto_data  # Actualiza el diccionario con el nuevo stock
                else:
                    print(f"Stock insuficiente para el producto ID: {producto_id}")
            else:
                print(f"Producto con ID: {producto_id} no encontrado.")
        print("\n🔍 [DEPURACIÓN] Estado final del stock antes de guardar:")
        for producto_id in productos_ids:
            producto_data = productos_dict.get(str(producto_id))
            if producto_data:
                print(f"  - Producto {producto_id}: Stock después de la venta -> {producto_data['stock']}")

        # Guardamos los productos con el stock actualizado en el archivo JSON
        self.guardar_datos_productos(productos_dict)  # Llamada al método para guardar los productos

    

    def guardar_datos_productos(self, productos_dict):
        """Guarda la información de productos en formato JSON como una lista."""
        try:
            # Convertir el diccionario de productos en una lista de objetos
            productos_lista = list(productos_dict.values())  

            with open('data/productos.json', 'w', encoding='utf-8') as archivo:
                json.dump(productos_lista, archivo, indent=4, ensure_ascii=False)

            print("Datos de productos guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar los productos: {e}")

    def obtener_todos(self):
        return {str(index + 1): venta for index, venta in enumerate(self.ventas)}
