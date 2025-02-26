import json
import os
import sys

class GestionProductos:
    def __init__(self, nombre_archivo='productos.json'): #quita la carpeta data, ya que la ruta base la agrega sys._MEIPASS
        self.nombre_archivo = nombre_archivo
        self.productos = self.cargar_datos()

    def _obtener_ruta_completa(self): #funcion para obtener la ruta del json.
        """Obtiene la ruta completa al archivo JSON."""
        if getattr(sys, 'frozen', False):
            # Estamos en un paquete PyInstaller
            ruta_base = sys._MEIPASS
        else:
            # Estamos ejecutando desde el código fuente
            ruta_base = os.path.abspath('.')
        return os.path.join(ruta_base, 'data', self.nombre_archivo) # importante que la carpeta se llame como la declaraste en add-data.

    def cargar_datos(self):
        """Carga los productos desde el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        if os.path.exists(ruta_completa):
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                try:
                    productos_dict = json.load(archivo)
                    return {str(k): v for k, v in productos_dict.items()}
                except json.JSONDecodeError:
                    print("❌ Error al leer JSON, inicializando un diccionario vacío.")
                    return {}
        else:
            return {}

    def guardar_datos(self):
        """Guarda los productos en el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        with open(ruta_completa, 'w', encoding='utf-8') as archivo:
            json.dump(self.productos, archivo, indent=4, ensure_ascii=False)

    # El resto de los métodos (existe_producto, agregar_producto, etc.) permanecen igual.
    # ...
    def existe_producto(self, id):
        """Verifica si un producto con el ID dado existe en el diccionario."""
        return str(id) in self.productos

    def agregar_producto(self, id, nombre, detalle,stock, precio):
        id_str = str(id)  # Convertimos el ID a string para mantener la consistencia

        if self.existe_producto(id_str):
            raise ValueError("Ya existe un producto con ese ID.")
    
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock debe ser un número entero positivo.")

        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número positivo.")
        
        # Agregar el producto al diccionario
        self.productos[id_str] = {
            'id': id,
            'nombre': nombre,
            'detalle': detalle,
            'stock': stock,
            'precio': precio
        }

        self.guardar_datos()

    def editar_producto(self, id, nombre=None, detalle=None,stock=None, precio=None):
        id_str = str(id)

        if id_str not in self.productos:
            print(f"❌ Error: Producto con ID {id} no encontrado")
            return

        producto = self.productos[id_str]
        print(f"📊 Datos actuales del producto {id}: {producto}")

        # Actualización de datos
        if nombre:
            producto["nombre"] = nombre
        if detalle is not None:
            producto["detalle"] = detalle
        if stock is not None:
            producto["stock"] = stock
        
        if precio is not None:
            producto["precio"] = precio

        print(f"✅ Datos actualizados del producto {id}: {producto}")
        self.guardar_datos()

    def eliminar_producto(self, id):
        id_str = str(id)

        if id_str not in self.productos:
            raise ValueError("No existe un producto con ese ID.")
        
        del self.productos[id_str]
        self.guardar_datos()

    def obtener_todos(self):
        return list(self.productos.values())  # Devuelve una lista con los valores del diccionario
