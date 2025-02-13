class Producto:
    def __init__(self, id, nombre, stock, precio):
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id}, Producto: {self.nombre}, Stock: {self.stock}, Precio: {self.precio}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "stock": self.stock,
            "precio": self.precio
        }