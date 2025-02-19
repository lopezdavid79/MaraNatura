import json  # Importa el módulo json
import os    # Importa el módulo os para trabajar con rutas

class GestionProductos:
    def __init__(self, nombre_archivo='data/productos.json'):  # Ruta relativa a la carpeta 'data'
        self.nombre_archivo = nombre_archivo
        self.productos = self.cargar_datos()  # Cargar los productos al iniciar

    def existe_producto(self, id_producto):
        return any(p["id"] == id_producto for p in self.productos)

    def cargar_datos(self):
        """Carga los productos desde el archivo JSON, asegurando que sea una lista."""
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo, 'r') as archivo:
                return json.load(archivo)
        else:
            return []  # Devuelve una lista vacía si no existe el archivo

    def guardar_datos(self):
        """Guarda los productos en el archivo JSON como lista."""
        with open(self.nombre_archivo, 'w') as archivo:
            json.dump(self.productos, archivo, indent=4)

    def agregar_producto(self, id, nombre, stock, precio):    
        # Validaciones
        if self.existe_producto(id):
            raise ValueError("Ya existe un producto con ese ID.")
    
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("El stock debe ser un número entero positivo.")

        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El precio debe ser un número positivo.")
        
        # Agregar el producto a la lista
        nuevo_producto = {
            'id': id,
            'nombre': nombre,
            'stock': stock,
            'precio': precio
        }
        self.productos.append(nuevo_producto)

        # Guardar cambios
        self.guardar_datos()

    def editar_producto(self, id, nombre=None, stock=None, precio=None):
        print(f"🔹 ID recibido: {id}, tipo: {type(id)}")

        # Convertir ID a entero si es necesario
        try:
            id = int(id)
        except ValueError:
            print(f"❌ Error: ID {id} no es un número válido")
            return

        # Buscar el producto por ID dentro de la lista de productos
        producto = next((p for p in self.productos if p["id"] == id), None)

        if not producto:
            print(f"❌ Error: Producto con ID {id} no encontrado")
            return

        print(f"📊 Datos actuales del producto {id}: {producto}")

        # Actualización de datos
        if nombre:
            producto["nombre"] = nombre
        if stock is not None:  # Permite stock = 0
            producto["stock"] = stock
        if precio is not None:  # Permite precio = 0
            producto["precio"] = precio

        print(f"✅ Datos actualizados del producto {id}: {producto}")

        # Guardar cambios
        self.guardar_datos()

    def eliminar_producto(self, id):
        if not self.existe_producto(id):
            raise ValueError("No existe un producto con ese ID.")
        
        # Eliminar producto de la lista
        self.productos = [p for p in self.productos if p["id"] != id]
        self.guardar_datos()

    def obtener_todos(self):
        return self.productos
