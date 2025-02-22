import json
from datetime import datetime

class Venta:
    def __init__(self, id, fecha, cliente, productos):
        self.id = id
        self.fecha = fecha or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cliente = cliente
        self.productos = productos

class GestionVentas:
    def __init__(self, nombre_archivo_ventas='data/ventas.json', nombre_archivo_productos='data/productos.json'):
        self.nombre_archivo_ventas = nombre_archivo_ventas
        self.nombre_archivo_productos = nombre_archivo_productos
        self.ventas = self.cargar_datos(self.nombre_archivo_ventas)
        self.productos = self.cargar_datos(self.nombre_archivo_productos)
        self.id_counter = self.get_next_id()

    def cargar_datos(self, nombre_archivo_ventas):
        try:
            with open(nombre_archivo_ventas, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Retorna una lista vacía en caso de error


    def guardar_datos(self):
        try:
            with open(self.nombre_archivo_ventas, 'w', encoding='utf-8') as archivo:
                json.dump(self.ventas, archivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar datos en : ")  # Asegúrate de descomentar esta línea

    def get_next_id(self):
        if self.ventas and isinstance(self.ventas, list):
            return max((venta.get('id', 0) for venta in self.ventas), default=0) + 1
        return 1

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
        for producto_id in productos_ids:
            producto_id_str = str(producto_id)  # Asegura que sea string para evitar errores

            if producto_id_str in productos_dict:
                producto_data = productos_dict[producto_id_str]
            
                if producto_data['stock'] > 0:
                    producto_data['stock'] -= 1
                    print(f"Stock actualizado para {producto_data['nombre']}: {producto_data['stock']} unidades restantes.")
                else:
                    print(f"Stock insuficiente para el producto: {producto_data['nombre']}")
            else:
                print(f"Producto no encontrado con ID: {producto_id}")

        self.guardar_productos(productos_dict)  # Guardar cambios en el archivo JSON

    def guardar_productos(self, productos_dict):
        try:
            with open(self.nombre_archivo_productos, 'w', encoding='utf-8') as archivo:
                json.dump(productos_dict, archivo, indent=4, ensure_ascii=False)
            print("Stock actualizado y guardado correctamente.")
        except Exception as e:
            print(f"Error al guardar productos: {e}")


    def obtener_todos(self):
        return {str(index + 1): venta for index, venta in enumerate(self.ventas)}
