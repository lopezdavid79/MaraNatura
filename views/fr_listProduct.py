import wx
import wx.lib.mixins.listctrl as listmix
from module.GestionProducto import GestionProductos

# Inicialización de la gestión de productos
gestion_productos = GestionProductos()

class ListaProductos(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id, title):
        super().__init__(parent, id, title=title, size=(500, 400))
        panel = wx.Panel(self)
        
        # Crear la lista de productos
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(460, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Producto', width=150)
        self.list_ctrl.InsertColumn(2, 'Stock', width=80)
        self.list_ctrl.InsertColumn(3, 'Precio', width=80)
        
        # Cargar productos en la lista
        self.cargar_productos()
        
        # Botón para agregar producto
        btn_nuevo = wx.Button(panel, label="Nuevo Producto", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        
        self.Show()
    
    def cargar_productos(self):
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevos productos
        productos = gestion_productos.obtener_todos()

        for id_producto, datos in productos.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_producto))
            self.list_ctrl.SetItem(index, 1, datos["nombre"])
            self.list_ctrl.SetItem(index, 2, str(datos["stock"]))
            self.list_ctrl.SetItem(index, 3, str(datos["precio"]))
    
    def abrir_dialogo_nuevo(self, event):
        dialogo = AgregarProductoDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_productos()  # Actualiza la lista después de agregar un producto
        dialogo.Destroy()
    
    def cerrar_ventana(self, event):
        self.Close()


class AgregarProductoDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Agregar Producto", size=(300, 250))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Campos de entrada
        vbox.Add(wx.StaticText(panel, label="ID Producto:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_id = wx.TextCtrl(panel)
        vbox.Add(self.txt_id, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        vbox.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_nombre = wx.TextCtrl(panel)
        vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        vbox.Add(wx.StaticText(panel, label="Stock:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_stock = wx.TextCtrl(panel)
        vbox.Add(self.txt_stock, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        vbox.Add(wx.StaticText(panel, label="Precio:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_precio = wx.TextCtrl(panel)
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
        self.Bind(wx.EVT_BUTTON, self.guardar_producto, btn_ok)

    def guardar_producto(self, event):
        id_producto = self.txt_id.GetValue()
        nombre = self.txt_nombre.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        if not id_producto or not nombre or not stock or not precio:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            stock = int(stock)
            precio = float(precio)
            gestion_productos.agregar_producto(id_producto, nombre, stock, precio)
            wx.MessageBox("Producto agregado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)  # Cierra el diálogo exitosamente
        except ValueError:
            wx.MessageBox("Stock debe ser un número entero y precio un número válido", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
