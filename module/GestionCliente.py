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

    def editar_cliente(self, id_cliente, nombre=None, dire=None, tel=None):
        """Edita los datos de un cliente dado su ID."""
        for cliente in self.clientes:
            if cliente["id"] == id_cliente:
                if nombre:
                    cliente["nombre"] = nombre
                if dire:
                    cliente["dire"] = dire
                if tel:
                    cliente["tel"] = tel
                self.guardar_datos()
                print(f"Cliente con ID {id_cliente} actualizado.")
                return True
        print(f"Cliente con ID {id_cliente} no encontrado.")
        return False

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

    