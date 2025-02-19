import json
from module.Clientes import Cliente  # Importa la clase Cliente


class GestionClientes:
    def __init__(self, nombre_archivo='data/clientes.json'):
        self.nombre_archivo = nombre_archivo
        self.clientes = self.cargar_datos()
        if not isinstance(self.clientes, list):  
            self.clientes = []  

    def cargar_datos(self):
        """Carga los clientes desde el archivo JSON."""
        try:
            with open(self.nombre_archivo, 'r') as archivo:
                return json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  

    def guardar_datos(self):
        """Guarda la lista de clientes en el archivo JSON."""
        with open(self.nombre_archivo, 'w') as archivo:
            json.dump(self.clientes, archivo, indent=4, ensure_ascii=False)

    def registrar_cliente(self, name_cliente, dire, tel):
        """Registra un nuevo cliente y lo guarda en la base de datos."""
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

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente por su ID."""
        cliente = self.buscar_cliente(id_cliente)
        if cliente:
            self.clientes.remove(cliente)
            self.guardar_datos()
            print(f"Cliente con ID {id_cliente} eliminado.")
            return True
        print(f"Cliente con ID {id_cliente} no encontrado.")
        return False


# Ejemplo de uso
if __name__ == "__main__":
    gestion_clientes = GestionClientes()

    # Obtener todos los clientes
    print("Lista de clientes:", gestion_clientes.obtener_todos())

    # Buscar un cliente
    cliente = gestion_clientes.buscar_cliente(1)
    print("Cliente encontrado:", cliente)

    