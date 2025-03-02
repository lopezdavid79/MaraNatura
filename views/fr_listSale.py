import sys
import os
import json
import re
import wx
import wx.lib.mixins.listctrl as listmix
from module.eventos import EVT_ACTUALIZAR_PRODUCTOS, ActualizarProductosEvent  # Importar el evento
from module.ReproductorSonido import ReproductorSonido
from module.GestionCliente import GestionClientes
from module.Ventas import GestionVentas, Venta
from module.Productos import Producto  # Asegurar que importamos la gestión de productos
from module.GestionProducto import  GestionProductos  # Asegurar que importamos la gestión de productos
import re
Producto  # Asegurar que importamos la gestión de productos
# Inicialización de la gestión de ventas y productos
gestion_clientes = GestionClientes()
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
            self.list_ctrl.SetItem(index, 3, str(datos["total"]))  # Ahora sí muestra el total
    
    def mostrar_detalle_ventas(self, event):
        
        index = event.GetIndex()
        id_venta = self.list_ctrl.GetItemText(index)

        ventas = gestion_ventas.obtener_todos()
        productos_dict=gestion_productos.obtener_todos()
        print(productos_dict)
        if not productos_dict:  # Verifica si el diccionario está vacío
            wx.MessageBox("No hay productos disponibles para mostrar.", "Error", wx.OK | wx.ICON_ERROR) 
            print("no hay productos ")
        if id_venta in ventas:
            datos = ventas[id_venta]
            print("Datos de la venta antes de pasar al diálogo:", datos)  # Depurar aquí
            dialogo = DetalleVentaDialog(self, id_venta, datos,productos_dict)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_ventas()  # Actualizar la lista
    
    def abrir_dialogo_nuevo(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarVentaDialog(self,gestion_ventas        )
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_ventas()  # Actualiza la lista después de agregar una venta        
        dialogo.Destroy()

    def cerrar_ventana(self, event):
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close()


class DetalleVentaDialog(wx.Dialog):
    def __init__(self, parent, id_venta, datos, productos_dict):
        super().__init__(parent, title="Detalle de Venta", size=(500, 400))
        
        # Guardamos el diccionario de productos y otros datos necesarios
        self.productos_dict = productos_dict  # Lista de productos
        self.id_venta = id_venta
        self.datos = datos
        
        # Panel de la ventana
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Mostrar detalles de la venta
        self.lista_productos = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.sizer.Add(self.lista_productos, 1, flag=wx.EXPAND|wx.ALL, border=5)
        
        self.lbl_cliente = wx.StaticText(panel, label=f"Cliente: {self.datos['cliente']}")
        self.sizer.Add(self.lbl_cliente, 0, flag=wx.ALL, border=5)

        self.lbl_total = wx.StaticText(panel, label=f"Total: ${self.datos['total']}")
        self.sizer.Add(self.lbl_total, 0, flag=wx.ALL, border=5)

        # Cargar los productos seleccionados en la venta
        self.cargar_productos()
    # Botón para cerrar el diálogo
        self.btn_cerrar = wx.Button(panel, label="Cerrar")
        self.sizer.Add(self.btn_cerrar, 0, flag=wx.CENTER|wx.ALL, border=5)

            # Bind the close button to the Close method
        self.btn_cerrar.Bind(wx.EVT_BUTTON, self.on_cerrar)

        panel.SetSizerAndFit(self.sizer)

    def cargar_productos(self):
        """Carga los productos en la lista del diálogo de detalle."""
        # Recorremos los productos asociados a la venta
        for producto_info in self.datos["productos"]:
            producto_id = producto_info["id_producto"]
            cantidad = producto_info["cantidad"]

            # Buscar el producto en self.productos_dict
            producto = next((p for p in self.productos_dict if p["id"] == producto_id), None)

            if producto:
                item_text = f"ID: {producto['id']} - {producto['nombre']} - Cantidad: {cantidad} - Precio: ${producto['precio']}"
                self.lista_productos.Append(item_text)
            else:
                print(f"Error: Producto con ID {producto_id} no encontrado.")
    def on_cerrar(self, event):
            self.EndModal(wx.ID_OK)  # Cierra el diálogo cuando se hace clic en el botón "Cerrar"
# Clase para agregar una nueva venta con selección de producto por nombre
import wx.lib.newevent
# 🔥 Crear un evento personalizado para actualizar la lista de productos en otra ventana
ActualizarProductosEvent, EVT_ACTUALIZAR_PRODUCTOS = wx.lib.newevent.NewEvent()

class AgregarVentaDialog(wx.Dialog):
    def __init__(self, parent,gestion_ventas):
        super().__init__(parent, title="Nueva Venta", size=(400, 400))      
        self.parent_productos = parent  # Referencia a la ventana de productos
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.nombre_archivo_productos = 'data/productos.json'
        self.gestion_ventas=gestion_ventas

        
        
                # Cliente
        vbox.Add(wx.StaticText(panel, label="Cliente:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_cliente = wx.SearchCtrl(panel, style=wx.TE_PROCESS_ENTER)
        vbox.Add(self.txt_cliente, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        self.lista_clientes = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.lista_clientes, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)
        self.txt_cliente.Bind(wx.EVT_TEXT, self.filtrar_clientes)
        self.lista_clientes.Bind(wx.EVT_LISTBOX, self.seleccionar_cliente)
        self.txt_cliente.Bind(wx.EVT_KEY_DOWN, self.on_key_cliente)  # Detectar Enter y navegación
        
        self.cargar_clientes()

        # Buscar Producto
        vbox.Add(wx.StaticText(panel, label="Buscar Producto:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_buscar_producto = wx.TextCtrl(panel)
        vbox.Add(self.txt_buscar_producto, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.txt_buscar_producto.Bind(wx.EVT_TEXT, self.filtrar_productos)

        # Lista de productos
        self.list_productos = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.list_productos, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)
        self.list_productos.SetFocus()  # Establecer el foco en la lista  
        self.list_productos.Bind(wx.EVT_LISTBOX_DCLICK, self.agregar_producto)
        self.list_productos.Bind(wx.EVT_KEY_DOWN, self.navegar_productos)

        # Productos seleccionados
        vbox.Add(wx.StaticText(panel, label="Productos seleccionados:"), flag=wx.LEFT | wx.TOP, border=10)
        self.list_productos_seleccionados = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.list_productos_seleccionados, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)

        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        self.btn_eliminar_producto = wx.Button(panel, label="Eliminar Producto")
        self.btn_agregar_producto = wx.Button(panel, label="Agregar Producto")
        hbox.Add(self.btn_eliminar_producto, flag=wx.LEFT, border=10)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.guardar_venta, btn_ok)
        self.btn_eliminar_producto.Bind(wx.EVT_BUTTON, self.eliminar_producto)
        self.btn_agregar_producto.Bind(wx.EVT_BUTTON, self.agregar_producto)

        self.productos_seleccionados = []
        self.productos_dict = self.cargar_productos()
        self.actualizar_lista_productos()
        
        self.lista_clientes.Bind(wx.EVT_LISTBOX_DCLICK, self.seleccionar_cliente)  # Doble clic para seleccionar

        # Total de la venta
        vbox.Add(wx.StaticText(panel, label="Total:"), flag=wx.LEFT | wx.TOP, border=10)
        self.lbl_total = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.lbl_total.SetValue("$0.00")  # Establecer el valor inicial
        vbox.Add(self.lbl_total, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.Layout()  # Layout inicial del diálogo
        self.txt_cliente.SetFocus()  # Establecer el foco en txt_cliente
        
        
        # 🔥 Atajos de teclado
        accel_tbl = wx.AcceleratorTable([
        (wx.ACCEL_CTRL, ord('G'), btn_ok.GetId()),  # Ctrl + G para guardar
        (wx.ACCEL_CTRL, ord('E'), self.btn_eliminar_producto.GetId()),  # Ctrl + E para eliminar producto
        (wx.ACCEL_CTRL, ord('A'), self.btn_agregar_producto.GetId()),  # Ctrl + E para eliminar producto
        (wx.ACCEL_CTRL, ord('B'), self.txt_buscar_producto.GetId()),  # Ctrl + B para buscar producto
    ])
        self.SetAcceleratorTable(accel_tbl)
 

    def ShowModal(self):
        self.productos_dict = self.cargar_productos()  # Recargar productos antes de mostrar
        self.actualizar_lista_productos()
        return super().ShowModal()

    def cargar_clientes(self):
        """Carga los clientes en la lista."""
        self.clientes_dict = gestion_clientes.obtener_todos()
        self.lista_clientes.Clear()
        for id_cliente, datos in self.clientes_dict.items():
            self.lista_clientes.Append(f"{datos['nombre']} ({datos['tel']})")
    
    def filtrar_clientes(self, event):
        """Filtra los clientes según el texto ingresado y mantiene la navegación."""
        filtro = self.txt_cliente.GetValue().lower()
        seleccion_anterior = self.lista_clientes.GetSelection()  # Guardar selección previa
        self.lista_clientes.Clear()

        for id_cliente, datos in self.clientes_dict.items():
            if filtro in datos['nombre'].lower():
                self.lista_clientes.Append(f"{datos['nombre']} ({datos['tel']})")

        if self.lista_clientes.GetCount() > 0:
            if seleccion_anterior == wx.NOT_FOUND:
                self.lista_clientes.SetSelection(0)  # Solo si antes no había selección
            self.lista_clientes.SetFocus()  # Mantiene la navegación con teclas
            # 🔥 Aquí forzamos la lectura de la selección en lectores de pantalla
            seleccion = self.lista_clientes.GetStringSelection()
            if seleccion:
                wx.CallAfter(self.lista_clientes.SetLabel, seleccion)

    
    def seleccionar_cliente(self, event=None):
        """Selecciona el cliente y devuelve el foco al campo de texto."""
        seleccion = self.lista_clientes.GetStringSelection()
        if seleccion:
            self.txt_cliente.SetValue(seleccion.split(' (')[0])  # Guarda solo el nombre
            self.lista_clientes.Hide()  # Oculta la lista después de seleccionar
            self.txt_cliente.SetFocus()  # Devuelve el foco al campo de texto

    def on_key_cliente(self, event):
        """Permite seleccionar el cliente solo con Enter (deshabilita las flechas)."""
        keycode = event.GetKeyCode()

        if keycode == wx.WXK_RETURN:  # Solo se selecciona con Enter
            self.seleccionar_cliente()
        else:
            event.Skip()  # Permite otros eventos del teclado, pero no las flechas
    def anunciar_seleccion(self):
        """Fuerza la lectura de la selección en lectores de pantalla."""
        seleccion = self.lista_clientes.GetStringSelection()
        if seleccion:
            wx.CallAfter(self.lista_clientes.SetLabel, seleccion)

    def cargar_productos(self):
        self.list_productos.Clear()
        productos = gestion_productos.obtener_productos()  # Suponiendo que devuelve el diccionario JSON
        #print("Tipo de 'productos':", type(productos))  
        productos_dict = {}  # Se crea un diccionario vacío.
        
        if productos:
            for producto in productos.values():  # Iteramos sobre los valores del diccionario
                item_text = f"Código: {producto['id']} - {producto['nombre']} - Stock: {producto['stock']} - Precio: ${producto['precio']}"
                self.list_productos.Append(item_text)
                productos_dict[producto['id']] = producto  # Usamos el ID como clave
        
        return productos_dict  # Se retorna el diccionario.
        
    def actualizar_lista_productos(self, filtro=""):
        self.list_productos.Clear()
        for producto in self.productos_dict.values():
            if filtro.lower() in producto["nombre"].lower():  # Busca en el nombre del producto
                item_text = f"ID: {producto['id']} - {producto['nombre']} - Stock: {producto['stock']} - Precio: ${producto['precio']}"
                self.list_productos.Append(item_text)



    def filtrar_productos(self, event):
        filtro = self.txt_buscar_producto.GetValue()
        self.actualizar_lista_productos(filtro)

#permite agregar un solo producto a la lista 
    
    def eliminar_producto(self, event):
        seleccion = self.list_productos_seleccionados.GetSelection()
        if seleccion != wx.NOT_FOUND:
            seleccion_str = self.list_productos_seleccionados.GetString(seleccion)
            self.productos_seleccionados.remove(seleccion_str)
            self.list_productos_seleccionados.Delete(seleccion)
            self.actualizar_total()

    def navegar_productos(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN:
            self.agregar_producto(None)
        elif keycode == wx.WXK_DELETE:
            self.eliminar_producto(None)
        elif keycode == wx.WXK_UP:
            current_selection = self.list_productos.GetSelection()
            if current_selection > 0:
                self.list_productos.SetSelection(current_selection - 1)
        elif keycode == wx.WXK_DOWN:
            current_selection = self.list_productos.GetSelection()
            if current_selection < self.list_productos.GetCount() - 1:
                self.list_productos.SetSelection(current_selection + 1)
        else:
            event.Skip()



#permite agregar varios productos
    def agregar_producto(self, event):
        seleccion = self.list_productos.GetStringSelection()
        if seleccion:
            match = re.search(r"ID:\s*(\d+)", seleccion)
            if match:
                producto_id = int(match.group(1))

                # Obtener el producto del diccionario de productos
                producto_info = next((p for p in self.productos_dict.values() if p["id"] == producto_id), None)

                if producto_info:
                    # Verificar el stock
                    if producto_info["stock"] > 0:
                        cantidad_str = wx.GetTextFromUser("Ingrese la cantidad:", "Cantidad", "1")

                        if cantidad_str:
                            if cantidad_str.isdigit():
                                cantidad = int(cantidad_str)

                                # Verificar que la cantidad no sea mayor al stock
                                if cantidad <= producto_info["stock"]:
                                    producto_seleccionado = {
                                        "id_producto": producto_id,
                                        "cantidad": cantidad,
                                        "descripcion": seleccion
                                    }

                                    producto_existente = next((p for p in self.productos_seleccionados if p["id_producto"] == producto_id), None)

                                    if producto_existente:
                                        producto_existente["cantidad"] += cantidad
                                        self.actualizar_lista_seleccionados()
                                    else:
                                        self.productos_seleccionados.append(producto_seleccionado)
                                        self.list_productos_seleccionados.Append(f"{seleccion} - Cantidad: {cantidad}")
                                    self.actualizar_total()
                                else:
                                    wx.MessageBox("La cantidad ingresada es mayor al stock disponible.", "Error", wx.OK | wx.ICON_ERROR)
                            else:
                                wx.MessageBox("Ingrese una cantidad válida.", "Error", wx.OK | wx.ICON_ERROR)
                        else:
                            print("El usuario canceló el ingreso de cantidad")
                    else:
                        wx.MessageBox("No hay stock disponible para este producto.", "Error", wx.OK | wx.ICON_ERROR)
                else:
                    wx.MessageBox("Producto no encontrado.", "Error", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("No se pudo extraer el ID del producto.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Seleccione un producto.", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_lista_seleccionados(self):
        self.list_productos_seleccionados.Clear()
        for producto in self.productos_seleccionados:
            self.list_productos_seleccionados.Append(f"{producto['descripcion']} - Cantidad: {producto['cantidad']}")

    def actualizar_total(self):
        total = 0
        for producto in self.productos_seleccionados:
            producto_id = producto["id_producto"]
            cantidad = producto["cantidad"]
            datos_producto = next((p for p in self.productos_dict.values() if p["id"] == producto_id), None)
            if datos_producto:
                total += float(datos_producto["precio"]) * cantidad

        self.lbl_total.SetLabel(f"${total:.2f}")
        self.Layout()

    def guardar_venta(self, event):
        cliente = self.txt_cliente.GetValue().strip()

        if not cliente or not self.productos_seleccionados:
            wx.MessageBox("Debe ingresar un cliente y al menos un producto", "Error", wx.OK | wx.ICON_ERROR)
            return

        productos_con_cantidad = []
        total_venta = 0

        for producto in self.productos_seleccionados:
            producto_id = producto["id_producto"]
            cantidad = producto["cantidad"]
            datos_producto = next((p for p in self.productos_dict.values() if p["id"] == producto_id), None)

            if datos_producto:
                productos_con_cantidad.append({
                    "id_producto": producto_id,
                    "cantidad": cantidad
                })
                total_venta += float(datos_producto["precio"]) * cantidad
            else:
                print(f"⚠️ Error: Producto con ID {producto_id} no encontrado en productos_dict.")

        if not productos_con_cantidad:
            wx.MessageBox("No se pudieron registrar los productos correctamente.", "Error", wx.OK | wx.ICON_ERROR)
            return

        self.gestion_ventas.registrar_venta(None, cliente, productos_con_cantidad, self.productos_dict, total_venta)
        
        ReproductorSonido.reproducir("Ok.wav")
        wx.MessageBox(f"Venta registrada con éxito. Total: ${total_venta:.2f}", "Éxito", wx.OK | wx.ICON_INFORMATION)
        # Crear el evento personalizado
        e = ActualizarProductosEvent()

        # Enviar el evento a la ventana de productos
        wx.PostEvent(self.parent_productos, e)# Crear el evento personalizado
        e = ActualizarProductosEvent()

        # Enviar el evento a la ventana de productos
        wx.PostEvent(self.parent_productos, ActualizarProductosEvent())
        # 🔥 Recargar productos después de la venta
        self.productos_dict = self.cargar_productos()  # Recargar desde JSON
        self.actualizar_lista_productos()  # Actualizar la interfaz con el stock nuevo
        self.EndModal(wx.ID_OK)