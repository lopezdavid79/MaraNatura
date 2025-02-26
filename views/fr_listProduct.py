import wx
import wx.lib.mixins.listctrl as listmix
from module.ReproductorSonido import ReproductorSonido
from module.GestionProducto import GestionProductos
from Views.fr_producto import VentanaProducto
# Inicialización de la gestión de productos
gestion_productos = GestionProductos()

class ListaProductos(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Nuevo Producto", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds) # Corrección


        panel = wx.Panel(self)
        
        # Crear la lista de productos
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(460, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Producto', width=150)
        self.list_ctrl.InsertColumn(2, 'Stock', width=80)
        self.list_ctrl.InsertColumn(3, 'Precio', width=80)
        
        # Cargar productos en la lista
        self.cargar_productos()
        
        # Evento para detectar tecla Enter
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_producto)

        # Botón para agregar producto
        btn_nuevo = wx.Button(panel, label="Nuevo Producto", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.on_close)
        #boton para actualizar 
        btn_actual= wx.Button(panel, label="Actualizar", pos=(150, 300))
        btn_actual.Bind(wx.EVT_BUTTON, self.actualizar_lista_productos)
        # Capturar eventos de teclado
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Show()
    
    def on_key_down(self, event):

        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("N"):  # Ctrl + N
            self.abrir_dialogo_nuevo(None)
        elif control_presionado and key_code == ord("C"):  # Ctrl + C -> Cerrar ventana
            self.on_close(None)
        event.Skip()  # Permitir que otros eventos se procesen




    def cargar_productos(self):
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevos productos
        productos = gestion_productos.obtener_todos()
        print("Productos obtenidos:", productos)  # 🛠️ Depuración

        if not isinstance(productos, list):  # Evitar errores si devuelve otra cosa
            print("❌ Error: `obtener_todos()` no devolvió una lista")
            return
            # Recorre la lista de productos
        for producto in productos:
            # Extrae el id y los datos del producto
            id_producto = producto["id"]
            datos = producto  # Todo el diccionario del producto
            
            # Inserta el producto en la lista de control
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_producto))
            self.list_ctrl.SetItem(index, 1, datos["nombre"])
            self.list_ctrl.SetItem(index, 2, str(datos["stock"]))
            self.list_ctrl.SetItem(index, 3, str(datos["precio"]))

    def mostrar_detalle_producto(self, event):
        index = event.GetIndex()
        id_producto = int(self.list_ctrl.GetItemText(index))  # Convierte el ID a entero

        # Obtener los detalles del producto
        productos = gestion_productos.obtener_todos()
        
        # Buscar el producto por ID en la lista
        producto = next((p for p in productos if p["id"] == id_producto), None)

        if producto:
            dialogo = DetalleProductoDialog(self, id_producto, producto)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_productos()  # Actualizar la lista después de la edición
        else:
            print(f"❌ Error: Producto con ID {id_producto} no encontrado")



    def abrir_dialogo_nuevo(self, event):
        producto_form = VentanaProducto(self, id=None, title="Nuevo Producto")  # self es el padre de la ventana
        producto_form.Bind(wx.EVT_CLOSE, self.cerrar_ventana)  # Detectar cierre
        producto_form.Show()  # Mostrar el formulario         
        ReproductorSonido.reproducir("screenCurtainOn.wav")
    def cerrar_ventana(self, event):
        print("Producto agregado, actualizando lista...")
        self.cargar_productos()
        event.Skip()  # Permitir que la ventana se cierre normalmente

    def actualizar_lista_productos(self,event):
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevos productos
        self.cargar_productos()   #Vuelve a cargar los productos del archivo JSON        
        #print("Productos obtenidos:", productos)  # 🛠️ Depuración
        
            
    def on_close(self, event):
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close()
                
class DetalleProductoDialog(wx.Dialog):
    def __init__(self, parent, id_producto, datos):
        super().__init__(parent, title="Detalle del Producto", size=(300, 250))
        self.id_producto = id_producto

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mostrar detalles
        vbox.Add(wx.StaticText(panel, label=f"ID: {id_producto}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Nombre: {datos['nombre']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Detalle: {datos.get('detalle', 'No disponible')}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Stock: {datos['stock']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Precio: {datos['precio']}"), flag=wx.LEFT | wx.TOP, border=10)

        # Botón para editar
        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_producto)
#boton para eliminar 
        btn_delete = wx.Button(panel, label="Eliminar")
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_producto)
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_delete, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def editar_producto(self, event):
        dialogo = EditarProductoDialog(self, self.id_producto)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
        dialogo.Destroy()



    def eliminar_producto(self, event):
            dialogo = EliminarProductoDialog(self, self.id_producto,gestion_productos)
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
        # Buscar el producto por ID en la lista
        producto = next((p for p in productos if p["id"] == id_producto), {})

        # Si el producto existe, cargamos sus datos
        if producto:
            # Campos editables
            vbox.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_nombre = wx.TextCtrl(panel, value=producto.get("nombre", ""))
            vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
            
            vbox.Add(wx.StaticText(panel, label="Detalle:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_detalle= wx.TextCtrl(panel, value=producto.get("detalle", ""))
            vbox.Add(self.txt_detalle, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

            vbox.Add(wx.StaticText(panel, label="Stock:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_stock = wx.TextCtrl(panel, value=str(producto.get("stock", "")))
            vbox.Add(self.txt_stock, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

            vbox.Add(wx.StaticText(panel, label="Precio:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_precio = wx.TextCtrl(panel, value=str(producto.get("precio", "")))
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
        else:
            wx.MessageBox(f"No se encontró el producto con ID {id_producto}", "Error", wx.OK | wx.ICON_ERROR)

    def guardar_cambios(self, event):
        nombre = self.txt_nombre.GetValue()
        detalle= self.txt_detalle.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        if not nombre or not detalle or not stock or not precio:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            stock = int(stock)
            precio = float(precio)
            gestion_productos.editar_producto(self.id_producto, nombre,detalle,stock, precio)
            wx.MessageBox("Producto actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except ValueError:
            wx.MessageBox("Stock debe ser un número entero y precio un número válido", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)



#eliminar producto
class EliminarProductoDialog(wx.Dialog):
    def __init__(self, parent, id_producto, gestion_productos):
        super().__init__(parent, title="Eliminar Producto", size=(300, 150))
        self.id_producto = id_producto
        self.parent = parent  # Guardamos la referencia al padre para actualizar la lista
        self.gestion_productos = gestion_productos  # Guardamos la referencia a la gestión de productos

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        productos = self.gestion_productos.obtener_todos()
        producto = next((p for p in productos if p["id"] == id_producto), None)

        if producto:
            mensaje = f"¿Estás seguro de que deseas eliminar el producto '{producto['nombre']}'?"
            vbox.Add(wx.StaticText(panel, label=mensaje), flag=wx.ALL, border=10)
            
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_ok = wx.Button(panel, wx.ID_OK, "Eliminar")
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
            hbox.Add(btn_cancel)
            
            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
            panel.SetSizer(vbox)
            
            self.Bind(wx.EVT_BUTTON, self.eliminar_producto, btn_ok)
        else:
            wx.MessageBox(f"No se encontró el producto con ID {id_producto}", "Error", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL)

    def eliminar_producto(self, event):
        try:
            self.gestion_productos.eliminar_producto(self.id_producto)
            wx.MessageBox("Producto eliminado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
            if hasattr(self.parent, "cargar_productos"):
                self.parent.cargar_productos()  # Actualizar la lista de productos en la ventana principal
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
