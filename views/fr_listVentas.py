import wx
import wx.lib.mixins.listctrl as listmix
from module.Ventas import GestionVentas,Venta

# Inicialización de la gestión de productos
gestion_ventas= GestionVentas()

class ListaVentas(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Nuevo Producto", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds) # Corrección


        panel = wx.Panel(self)
        
        # Crear la lista de productos
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(460, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Fecha', width=80)
        self.list_ctrl.InsertColumn(2, 'Cliente', width=150)        
        self.list_ctrl.InsertColumn(3, 'Total', width=80)
        
        # Cargar ventas en la lista
        self.cargar_ventas()
        
        # Evento para detectar tecla Enter
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_ventas)

        # Botón para agregar venta
        btn_nuevo = wx.Button(panel, label="Nueva Venta", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        
        self.Show()
    
    def cargar_ventas(self):
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevos productos
        ventas = gestion_ventas.obtener_todos()

        for id_venta, datos in ventas.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_venta))
            self.list_ctrl.SetItem(index, 1, datos["fecha"])
            self.list_ctrl.SetItem(index, 2, str(datos["cliente"]))
            self.list_ctrl.SetItem(index, 3, str(datos["total"]))
    
    def mostrar_detalle_ventas(self, event):
        index = event.GetIndex()
        id_venta= self.list_ctrl.GetItemText(index)

        # Obtener los detalles del producto
        ventas = gestion_ventas.obtener_todos()
        if id_venta in ventas:
            datos = ventas[id_venta]
            dialogo = DetalleVentaDialog(self, id_venta, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_productos()  # Actualizar la lista después de la edición
    
    def abrir_dialogo_nuevo(self, event):
        dialogo = AgregarventaDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_venta()  # Actualiza la lista después de agregar un producto
        dialogo.Destroy()
    
    def cerrar_ventana(self, event):
        self.Close()


class DetalleVentaDialog(wx.Dialog):
    def __init__(self, parent, id_venta, datos):
        super().__init__(parent, title="Detalle del Producto", size=(300, 250))
        self.id_venta= id_venta

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mostrar detalles
        vbox.Add(wx.StaticText(panel, label=f"ID: {id_venta}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Fecha: {datos['fecha']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Cliente: {datos['cliente']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Total: {datos['total']}"), flag=wx.LEFT | wx.TOP, border=10)
"""
        # Botón para editar
        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_producto)

        # Botón para cerrar
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def editar_producto(self, event):
        dialogo = EditarProductoDialog(self, self.id_producto)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
        dialogo.Destroy()


class EditarProductoDialog(wx.Dialog):
    def __init__(self, parent, id_producto):
        super().__init__(parent, title="Editar Producto", size=(300, 250))
        self.id_producto = id_producto

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        productos = gestion_productos.obtener_todos()
        datos = productos.get(id_producto, {})

        # Campos editables
        vbox.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_nombre = wx.TextCtrl(panel, value=datos.get("nombre", ""))
        vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Stock:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_stock = wx.TextCtrl(panel, value=str(datos.get("stock", "")))
        vbox.Add(self.txt_stock, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Precio:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_precio = wx.TextCtrl(panel, value=str(datos.get("precio", "")))
        vbox.Add(self.txt_precio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

        # Bind para el botón "Guardar"
        self.Bind(wx.EVT_BUTTON, self.guardar_cambios, btn_ok)

    def guardar_cambios(self, event):
        nombre = self.txt_nombre.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        if not nombre or not stock or not precio:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            stock = int(stock)
            precio = float(precio)
            gestion_productos.editar_producto(self.id_producto, nombre, stock, precio)
            wx.MessageBox("Producto actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except ValueError:
            wx.MessageBox("Stock debe ser un número entero y precio un número válido", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
"""