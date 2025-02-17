import json



class Cliente:
    def __init__(self, id, nombre , dire, tel):
        self.id = id
        self.nombre= nombre # Corrección: asignar correctamente
        self.dire = dire
        self.tel = tel

    def __str__(self):
        return f"Cliente(ID: {self.id}, Nombre: {self.nombre}, Dirección: {self.dire}, Teléfono: {self.tel})"

    def to_json(self):
        """Convierte el objeto Cliente a JSON"""
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """Crea un objeto Cliente a partir de un JSON"""
        data = json.loads(json_str)
        return cls(**data)

