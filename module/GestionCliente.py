import json
import os
import sys

from module.Clientes import Cliente  # Importa la clase Cliente


class GestionClientes:
    def __init__(self, nombre_archivo='clientes.json'):
        self.nombre_archivo = nombre_archivo
        self.clientes = self.cargar_datos()
        if not isinstance(self.clientes, list):  
            self.clientes = []  



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
        """Carga los clientes desde el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        if os.path.exists(ruta_completa):
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                try:
                    clientes_lista = json.load(archivo)  # Carga como lista
                    return clientes_lista
                except json.JSONDecodeError:
                    print("❌ Error al leer JSON, inicializando una lista vacía.")
                    return []
        else:
            return []

    def guardar_datos(self):
        """Guarda la lista de clientes en el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        with open(ruta_completa, 'w', encoding='utf-8') as archivo:
            json.dump(self.clientes, archivo, indent=4, ensure_ascii=False)

    """Registra un nuevo cliente y lo guarda en la base de datos."""
    def registrar_cliente(self, name_cliente, dire, tel):    
        nuevo_id = len(self.clientes) + 1  
        nuevo_cliente = Cliente(nuevo_id, name_cliente, dire, tel)

        cliente_dict = nuevo_cliente.__dict__
        self.clientes.append(cliente_dict)  
        self.guardar_datos()  

        print(f"Cliente registrado: {cliente_dict}")
        return nuevo_cliente

    def editar_cliente(self, id, nombre=None, tel=None, dire=None):
        print(f"🔹 ID recibido: {id}, tipo: {type(id)}")
    
        # Convertir ID a entero si es necesario
        try:
            id = int(id)
        except ValueError:
            print(f"❌ Error: ID {id} no es un número válido")
            return

        # Verificar el tipo de self.clientes
        if not isinstance(self.clientes, list):
            print("⚠️ Error: self.clientes no es una lista")
            return

        # Buscar el cliente por ID dentro de la lista
        cliente = next((c for c in self.clientes if c["id"] == id), None)

        if not cliente:
            print(f"❌ Error: Cliente con ID {id} no encontrado")
            return

        print(f"📊 Datos actuales del cliente {id}: {cliente}")

        # Actualización de datos
        if nombre:
            cliente["nombre"] = nombre
        if tel:
            cliente["tel"] = tel
        if dire:
            cliente["dire"] = dire

        print(f"✅ Datos actualizados del cliente {id}: {cliente}")

        # Guardar cambios
        self.guardar_datos()

    def obtener_todos(self):
        """Devuelve todos los clientes como un diccionario indexado."""
        return {str(index + 1): cliente for index, cliente in enumerate(self.clientes)}


    def buscar_cliente(self, id_cliente):
        """Busca un cliente por su ID y devuelve su información."""
        for cliente in self.clientes:
            if cliente["id"] == id_cliente:
                return cliente
        return None  # Devuelve None si no se encuentra

    """Elimina un cliente por su ID en una lista de diccionarios."""
    def eliminar_cliente(self, id_cliente):
        print(f"Tipo de self.clientes: {type(self.clientes)}")
        print(f"Clientes actuales: {self.clientes}")
        
        id_cliente = int(id_cliente)  # Convertir a entero porque los IDs en la lista parecen ser enteros
        
        # Buscar el cliente en la lista
        cliente = next((c for c in self.clientes if c["id"] == id_cliente), None)

        if cliente:
            self.clientes.remove(cliente)  # Eliminar cliente de la lista
            self.guardar_datos()
            print(f"Cliente con ID {id_cliente} eliminado.")
            return True

        print(f"Cliente con ID {id_cliente} no encontrado.")
        return False
