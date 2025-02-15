import wx

from Views.fr_listProduct import ListaProductos
from Views.fr_producto import VentanaProducto
from Views.fr_listSale import ListSale


class Principal(wx.Frame):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        # Crear la barra de menú
        menubar = wx.MenuBar()

        # Crear el menú "Archivo"
        file_menu = wx.Menu()
        new_product_item = wx.MenuItem(file_menu, wx.ID_ANY, "Nuevo producto")
        
        file_menu.Append(new_product_item)
        file_menu.AppendSeparator()  # Separador
        list_product_item = wx.MenuItem(file_menu, wx.ID_ANY, "Lista de  Productos")
        file_menu.Append(list_product_item)
        file_menu.AppendSeparator()  # Separador
        exit_item = wx.MenuItem(file_menu, wx.ID_ANY, "Salir")
        file_menu.Append(exit_item)

        # Crear el menú "Ventas"
        sales_menu = wx.Menu()
        new_sale_item = wx.MenuItem(sales_menu, wx.ID_ANY, "Lista de Ventas")
        sales_menu.Append(new_sale_item)

        # Añadir los menús a la barra de menú
        menubar.Append(file_menu, "Archivo")
        menubar.Append(sales_menu, "Ventas")
        self.SetMenuBar(menubar)

        # Enlazar los eventos de los menús
        self.Bind(wx.EVT_MENU, self.on_new_product, new_product_item)
        self.Bind(wx.EVT_MENU, self.on_list_product,list_product_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_list_sale, new_sale_item)

        self.SetTitle("Gestión Ventas de Mara Natura")
        self.SetSize((600, 400))
        self.Centre()

    def on_new_product(self, event):
        # Aquí se abriría el formulario para agregar un nuevo producto
        producto_form = VentanaProducto(self, id=None, title="Nuevo Producto")  # self es el padre de la ventana
        producto_form.Show()  # Mostrar el formulario 
        

    def on_list_product(self, event):
        # Aquí se abriría el formulario para listado producto
        list_producto_form = ListaProductos(self, id=None, title="Lista de Productos")  # self es el padre de la ventana
        list_producto_form.Show()  # Mostrar el formulario 
        

    def on_list_sale(self, event):
        # Aquí se abriría el formulario para listado de ventas.
        list_sale_form = ListSale(self, id=None, title="Lista de Ventas")  # self es el padre de la ventana
        list_sale_form.Show()  # Mostrar el formulario 
        


    def on_exit(self, event):
        self.Close()

    
   