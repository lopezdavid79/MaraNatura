import wx
import wx.lib.mixins.listctrl as listmix
from module.Ventas import GestionVentas, Venta
from module.Productos import Producto  # Asegurar que importamos la gestión de productos
from module.GestionProducto import  GestionProductos  # Asegurar que importamos la gestión de productos
Producto  # Asegurar que importamos la gestión de productos
# Inicialización de la gestión de ventas y productos
gestion_productos = GestionProductos()
gestion_ventas = GestionVentas()

class ListSale(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Ventas", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)
        
        # Crear la lista de ventas
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(460, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Fecha', width=100)
        self.list_ctrl.InsertColumn(2, 'Cliente', width=150)        
        self.list_ctrl.InsertColumn(3, 'Total', width=100)
        
        self.cargar_ventas()
        
        # Evento para doble clic en una venta
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_ventas)

        # Botón para agregar venta
        btn_nuevo = wx.Button(panel, label="Nueva Venta", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        
        self.Show()
    
    def cargar_ventas(self):
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevas ventas
        ventas = gestion_ventas.obtener_todos()

        for id_venta, datos in ventas.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_venta))
            self.list_ctrl.SetItem(index, 1, datos["fecha"])
            self.list_ctrl.SetItem(index, 2, str(datos["cliente"]))
            #self.list_ctrl.SetItem(index, 3, str(datos["total"]))  # Ahora sí muestra el total
    
    def mostrar_detalle_ventas(self, event):
        index = event.GetIndex()
        id_venta = self.list_ctrl.GetItemText(index)

        ventas = gestion_ventas.obtener_todos()
        if id_venta in ventas:
            datos = ventas[id_venta]
            dialogo = DetalleVentaDialog(self, id_venta, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_ventas()  # Actualizar la lista
    
    def abrir_dialogo_nuevo(self, event):
        dialogo = AgregarVentaDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_ventas()  # Actualiza la lista después de agregar una venta
        dialogo.Destroy()
    
    def cerrar_ventana(self, event):
        self.Close()


class DetalleVentaDialog(wx.Dialog):
    def __init__(self, parent, id_venta, datos):
        super().__init__(parent, title="Detalle de la Venta", size=(300, 250))
        self.id_venta = id_venta

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mostrar detalles
        vbox.Add(wx.StaticText(panel, label=f"ID: {id_venta}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Fecha: {datos['fecha']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Cliente: {datos['cliente']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Total: {datos['total']}"), flag=wx.LEFT | wx.TOP, border=10)

        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")
        vbox.Add(btn_cerrar, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)


# Clase para agregar una nueva venta con selección de producto por nombre

class AgregarVentaDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Nueva Venta", size=(400, 400))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(panel, label="Cliente:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_cliente = wx.TextCtrl(panel)
        vbox.Add(self.txt_cliente, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        # Entrada para buscar productos
        vbox.Add(wx.StaticText(panel, label="Buscar Producto:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_buscar_producto = wx.TextCtrl(panel)
        vbox.Add(self.txt_buscar_producto, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.txt_buscar_producto.Bind(wx.EVT_TEXT, self.filtrar_productos)
        # Lista de productos filtrados
        self.list_productos = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.list_productos, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)
        self.list_productos.Bind(wx.EVT_LISTBOX_DCLICK, self.agregar_producto)
        self.list_productos.Bind(wx.EVT_KEY_DOWN, self.navegar_productos)
        self.productos_dict = self.cargar_productos()
        self.actualizar_lista_productos()
        # Lista de productos agregados
        vbox.Add(wx.StaticText(panel, label="Productos seleccionados:"), flag=wx.LEFT | wx.TOP, border=10)
        self.list_productos_seleccionados = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.list_productos_seleccionados, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.guardar_venta, btn_ok)
        self.productos_seleccionados = []
    
    def cargar_productos(self):
        productos_lista = gestion_productos.obtener_todos()
        print("Productos obtenidos:", productos_lista)  # Depuración

        # Convertir a formato correcto
        self.productos_dict = {datos["nombre"]: datos for datos in productos_lista.values()}
        return self.productos_dict

    def actualizar_lista_productos(self, filtro=""):
        self.list_productos.Clear()
        for nombre, datos in self.productos_dict.items():
            if filtro.lower() in nombre.lower():
                
                item_text = f"{nombre} - Stock: {datos['stock']} - Precio: ${datos['precio']}"
                self.list_productos.Append(item_text)
    def filtrar_productos(self, event):
        filtro = self.txt_buscar_producto.GetValue()
        self.actualizar_lista_productos(filtro)

        
    def agregar_producto(self, event):
        seleccion = self.list_productos.GetStringSelection()
        if seleccion and seleccion not in self.productos_seleccionados:
            self.productos_seleccionados.append(seleccion)
            self.list_productos_seleccionados.Append(seleccion)
    def eliminar_producto(self, event):
        seleccion = self.list_productos_seleccionados.GetStringSelection()
        if seleccion:
            self.productos_seleccionados.remove(seleccion)
            self.list_productos_seleccionados.Delete(self.list_productos_seleccionados.GetSelection())
    def navegar_productos(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN:  # Enter selecciona el producto
            self.agregar_producto(None)
        elif keycode == wx.WXK_DELETE:  # Suprimir elimina el producto seleccionado
            self.eliminar_producto(None)
        else:
            event.Skip()

    def guardar_venta(self, event):
        cliente = self.txt_cliente.GetValue().strip()
        if not cliente or not self.productos_seleccionados:
            wx.MessageBox("Debe ingresar un cliente y al menos un producto", "Error", wx.OK | wx.ICON_ERROR)
            return
        productos_ids = [self.productos_dict[p]["id"] for p in self.productos_seleccionados]
        gestion_ventas.registrar_venta(None, cliente, productos_ids, self.productos_dict)
        wx.MessageBox("Venta registrada con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

 
 