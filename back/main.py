import os
from module.Productos import  Producto
from  module.GestionProducto import GestionProductos
from  module.Ventas import GestionVentas, Venta
# Rutas a los archivos JSON (relativas a la carpeta 'data')
productos_archivo = os.path.join("data", "productos.json") #une las rutas a los archivos json
ventas_archivo = os.path.join("data", "ventas.json")

# Inicialización
gestion_productos = GestionProductos()
gestion_ventas = GestionVentas()

# --- Menú ---
while True:
    print("\n--- Menú ---")
    print("1. Agregar producto")
    print("2. Modificar producto")
    print("3. Eliminar producto")
    print("4. Registrar venta")
    print("5. Mostrar productos")
    print("6. Mostrar ventas")
    print("7. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == '1':
        id = input("ID: ")
        nombre = input("Nombre: ")
        stock = int(input("Stock: "))
        precio = float(input("Precio: "))
        try:
            gestion_productos.agregar_producto(id, nombre, stock, precio)
            print("Producto agregado con éxito.")
        except ValueError as e:
            print(f"Error al agregar producto: {e}")

    elif opcion == '2':
        id = input("ID del producto a modificar: ")
        try:
            datos_modificar = {}
            nuevo_nombre = input("Nuevo nombre (dejar en blanco para no modificar): ")
            if nuevo_nombre:
                datos_modificar['nombre'] = nuevo_nombre
            nuevo_stock = input("Nuevo stock (dejar en blanco para no modificar): ")
            if nuevo_stock:
                datos_modificar['stock'] = int(nuevo_stock)
            nuevo_precio = input("Nuevo precio (dejar en blanco para no modificar): ")
            if nuevo_precio:
                datos_modificar['precio'] = float(nuevo_precio)

            if datos_modificar:
                gestion_productos.modificar_producto(id, **datos_modificar)
                print("Producto modificado con éxito.")
            else:
                print("No se especificaron datos para modificar.")
        except ValueError as e:
            print(f"Error al modificar producto: {e}")

    elif opcion == '3':
        id = input("ID del producto a eliminar: ")
        try:
            gestion_productos.eliminar_producto(id)
            print("Producto eliminado con éxito.")
        except ValueError as e:
            print(f"Error al eliminar producto: {e}")

    elif opcion == '4':
        fecha = input("fecha: ")
        cliente = input("Nombre del cliente: ")
        productos_ids = input("IDs de los productos (separados por comas): ").split(',')
        try:
            nueva_venta = gestion_ventas.registrar_venta(fecha,cliente, productos_ids, gestion_productos.productos)
            print("Venta registrada con éxito:", nueva_venta.__dict__)
        except ValueError as e:
            print(f"Error al registrar la venta: {e}")

    elif opcion == '5':
        for id, datos in gestion_productos.productos.items():
            producto = Producto(id, datos['nombre'], datos['stock'], datos['precio'])
            print(producto)

    elif opcion == '6':
        for venta_data in gestion_ventas.ventas:
            venta = Venta(**venta_data)  # Crea un objeto Venta a partir del diccionario
            productos_dict = {id: Producto(id, datos['nombre'], datos['stock'], datos['precio']) for id, datos in gestion_productos.productos.items()}
            print(f"Cliente: {venta.cliente}, Total: {venta.calcular_total(productos_dict)}")
            for producto_id in venta.productos:
                producto = productos_dict.get(producto_id)
                if producto:
                    print(f"  - {producto.nombre}")

    elif opcion == '7':
        break
    else:
        print("Opción no válida.")