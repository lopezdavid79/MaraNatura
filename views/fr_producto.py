import datetime
import os
from module.Productos import Producto
from module.GestionProducto import GestionProductos
from module.Ventas import GestionVentas, Venta

# Inicialización
gestion_productos = GestionProductos()

import wx

class VentanaProducto(wx.Frame):
    def __init__(self, parent, id=None, title="Nuevo Producto", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds) # Corrección


        self.id = id  # Guarda el ID (puede ser None si es un nuevo producto)
        self.SetTitle(title) # Usa el título proporcionado
        # Panel principal
        panel = wx.Panel(self)

        # Etiquetas y campos de entrada
        wx.StaticText(panel, label="ID:", pos=(10, 10))
        self.txt_id = wx.TextCtrl(panel, pos=(100, 10))

        wx.StaticText(panel, label="Producto:", pos=(10, 40))
        self.txt_producto = wx.TextCtrl(panel, pos=(100, 40))

        wx.StaticText(panel, label="Stock:", pos=(10, 70))
        self.txt_stock = wx.TextCtrl(panel, pos=(100, 70))

        wx.StaticText(panel, label="Precio:", pos=(10, 100))
        self.txt_precio = wx.TextCtrl(panel, pos=(100, 100))

        # Botón de guardar
        btn_guardar = wx.Button(panel, label="Guardar", pos=(150, 150))
        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_producto)
        # Botón de cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(250, 150))  # Posición ajustada
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        # Área de mensajes
        self.lbl_mensaje = wx.StaticText(panel, label="", pos=(10, 200))

        self.Show()

    def guardar_producto(self, event):
        id_producto = self.txt_id.GetValue()
        nombre = self.txt_producto.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        # Validación de campos
        if not id_producto or not nombre or not stock or not precio:
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.")
            return

        try:
            stock = int(stock)
            precio = float(precio)
            id_producto = int(id_producto)  # Convierte id_producto a entero
        except ValueError:
            self.mostrar_mensaje("Error: ID, Stock y precio deben ser números.")
            return
        # Validación de ID
        if id_producto <= 0:
            self.mostrar_mensaje("Error: El ID debe ser un número positivo.")
            return

        # Verificar si el ID ya existe
        if gestion_productos.existe_producto(id_producto):
            self.mostrar_mensaje("Error: Ya existe un producto con ese ID.")
            return
        gestion_productos.agregar_producto(id_producto, nombre, stock, precio)

        print(f"Producto guardado: ID={id_producto}, Producto={nombre}, Stock={stock}, Precio={precio}")  # Usa 'nombre' en lugar de 'nombre_producto'
        wx.MessageBox(f"Venta registrada con éxito. ", "Éxito", wx.OK | wx.ICON_INFORMATION)

        # Limpiar campos
        self.txt_id.SetValue("")
        self.txt_producto.SetValue("")
        self.txt_stock.SetValue("")
        self.txt_precio.SetValue("")


    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):  # Tipo de mensaje opcional
        wx.MessageBox(mensaje, "Error", style=tipo)  # Usar wx.MessageBox

    
    def cerrar_ventana(self, event):
        self.Close()  # Cierra la ventana
