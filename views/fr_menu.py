import wx
from Views.fr_listProduct import ListaProductos
from Views.fr_producto import VentanaProducto
from Views.fr_listSale import ListSale
from Views.fr_cliente import VentanaCliente  # Importamos la ventana de clientes
from Views.fr_listClient  import ListaClientes  # Importamos la gestión de clientes

class Principal(wx.Frame):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        # Crear la barra de menú
        menubar = wx.MenuBar()

        # Crear el menú "Archivo"
        file_menu = wx.Menu()
        new_product_item = wx.MenuItem(file_menu, wx.ID_ANY, "Nuevo producto")
        file_menu.Append(new_product_item)
        file_menu.AppendSeparator()
        list_product_item = wx.MenuItem(file_menu, wx.ID_ANY, "Lista de Productos")
        file_menu.Append(list_product_item)
        file_menu.AppendSeparator()
        exit_item = wx.MenuItem(file_menu, wx.ID_ANY, "Salir")
        file_menu.Append(exit_item)

        # Crear el menú "Clientes"
        client_menu = wx.Menu()
        new_client_item = wx.MenuItem(client_menu, wx.ID_ANY, "Nuevo Cliente")
        client_menu.Append(new_client_item)
        client_menu.AppendSeparator()
        list_client_item = wx.MenuItem(client_menu, wx.ID_ANY, "Lista de Clientes")
        client_menu.Append(list_client_item)

        # Crear el menú "Ventas"
        sales_menu = wx.Menu()
        new_sale_item = wx.MenuItem(sales_menu, wx.ID_ANY, "Lista de Ventas")
        sales_menu.Append(new_sale_item)

        # Añadir los menús a la barra de menú
        menubar.Append(file_menu, "Archivo")
        menubar.Append(client_menu, "Clientes")  # Agregamos la sección de clientes
        menubar.Append(sales_menu, "Ventas")
        self.SetMenuBar(menubar)

        # Enlazar los eventos de los menús
        self.Bind(wx.EVT_MENU, self.on_new_product, new_product_item)
        self.Bind(wx.EVT_MENU, self.on_list_product, list_product_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_new_client, new_client_item)  # Nuevo Cliente
        self.Bind(wx.EVT_MENU, self.on_list_client, list_client_item)  # Lista de Clientes
        self.Bind(wx.EVT_MENU, self.on_list_sale, new_sale_item)

        self.SetTitle("Gestión Ventas de Mara Natura")
        self.SetSize((600, 400))
        self.Centre()

    def on_new_product(self, event):
        """Abre el formulario para agregar un nuevo producto."""
        producto_form = VentanaProducto(self, id=None, title="Nuevo Producto")
        producto_form.Show()

    def on_list_product(self, event):
        """Abre el formulario de lista de productos."""
        list_producto_form = ListaProductos(self, id=None, title="Lista de Productos")
        list_producto_form.Show()

    def on_new_client(self, event):
        """Abre el formulario para agregar un nuevo cliente."""
        cliente_form = VentanaCliente(self, id=None, title="Nuevo Cliente")
        cliente_form.Show()

    def on_list_client(self, event):
        
        list_client_form = ListaClientes(self, id=None, title="Lista de Clientes")
        list_client_form.Show()

    def on_list_sale(self, event):
        """Abre el formulario de lista de ventas."""
        list_sale_form = ListSale(self, id=None, title="Lista de Ventas")
        list_sale_form.Show()

    def on_exit(self, event):
        """Cierra la aplicación."""
        self.Close()
