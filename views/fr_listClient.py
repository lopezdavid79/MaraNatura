import re
import sys
import wx
import wx.lib.mixins.listctrl as listmix
from module.ReproductorSonido import ReproductorSonido
from module.GestionCliente import GestionClientes
#from Views.fr_cliente import VentanaCliente# Inicialización de la gestión de clientes
gestion_clientes = GestionClientes()

class ListaClientes(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Gestión de Clientes", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)

        # Crear la lista de clientes
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(460, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Nombre', width=150)
        self.list_ctrl.InsertColumn(2, 'Teléfono', width=100)
        self.list_ctrl.InsertColumn(3, 'Dirección', width=150)

        # Cargar clientes en la lista
        self.cargar_clientes()

        # Evento para detectar doble clic en un cliente
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_cliente)

        # Botón para agregar cliente
        btn_nuevo = wx.Button(panel, label="Nuevo Cliente", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)

        # Botón para cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)

# Botón para actualizar la lista de clientes
        btn_actualizar = wx.Button(panel, label="Actualizar ", pos=(175, 300))
        btn_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_lista)

        self.Show()


#actualiza la lista de clientes 
    def actualizar_lista(self, event):
        """Recarga la lista de clientes en la interfaz."""
        self.cargar_clientes()
        print("Lista actualizada en la interfaz")
        sys.stdout.flush()  # <-- Fuerza la salida en la consola
        ReproductorSonido.reproducir("refresh.wav")

    def cargar_clientes(self):
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevos clientes
        clientes = gestion_clientes.obtener_todos()

        for id_cliente, datos in clientes.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_cliente))
            self.list_ctrl.SetItem(index, 1, datos["nombre"])
            self.list_ctrl.SetItem(index, 2, datos["tel"])
            self.list_ctrl.SetItem(index, 3, datos["dire"])

    def mostrar_detalle_cliente(self, event):
        index = event.GetIndex()
        id_cliente = self.list_ctrl.GetItemText(index)

        # Obtener los detalles del cliente
        clientes = gestion_clientes.obtener_todos()
        if id_cliente in clientes:
            datos = clientes[id_cliente]
            dialogo = DetalleClienteDialog(self, id_cliente, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_clientes()  # Actualizar la lista después de la edición

    def abrir_dialogo_nuevo(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarClienteDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_clientes()  # Actualiza la lista después de agregar una venta
        dialogo.Destroy()
    

    def cerrar_ventana(self, event):
        ReproductorSonido.reproducir("screenCurtainOff  .wav")
        self.Close()


class DetalleClienteDialog(wx.Dialog):
    def __init__(self, parent, id_cliente, datos):
        super().__init__(parent, title="Detalle del Cliente", size=(300, 250))
        self.id_cliente = id_cliente

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mostrar detalles
        vbox.Add(wx.StaticText(panel, label=f"ID: {id_cliente}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Nombre: {datos['nombre']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Teléfono: {datos['tel']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Dirección: {datos['dire']}"), flag=wx.LEFT | wx.TOP, border=10)

        # Botón para editar
        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_cliente)
#eliminar cliente
        btn_delete = wx.Button(panel, label="Eliminar")
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_cliente)
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def editar_cliente(self, event):
        dialogo = EditarClienteDialog(self, self.id_cliente)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
        dialogo.Destroy()
    def eliminar_cliente(self, event):
            dialogo = EliminarClienteDialog(self, self.id_cliente,gestion_clientes)
            if dialogo.ShowModal() == wx.ID_OK:
                self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
            dialogo.Destroy()


class EditarClienteDialog(wx.Dialog):
    def __init__(self, parent, id_cliente):
        super().__init__(parent, title="Editar Cliente", size=(300, 250))
        self.id_cliente = id_cliente

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        clientes = gestion_clientes.obtener_todos()
        datos = clientes.get(id_cliente, {})

        # Campos editables
        vbox.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_nombre = wx.TextCtrl(panel, value=datos.get("nombre", ""))
        vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Teléfono:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_telefono = wx.TextCtrl(panel, value=datos.get("tel", ""))
        vbox.Add(self.txt_telefono, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Dirección:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_dire= wx.TextCtrl(panel, value=datos.get("dire", ""))
        vbox.Add(self.txt_dire, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

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
        tel = self.txt_telefono.GetValue()
        dire = self.txt_dire.GetValue()

        if not nombre or not tel or not dire:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            gestion_clientes.editar_cliente(self.id_cliente, nombre, tel, dire)
            wx.MessageBox("Cliente actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


#eliminar cliente
#eliminar cliente
class EliminarClienteDialog(wx.Dialog):
    def __init__(self, parent, id_cliente, gestion_clientes):
        super().__init__(parent, title="Eliminar Cliente", size=(300, 150))
        self.id_cliente = id_cliente
        self.parent = parent  # Guardamos la referencia al padre para actualizar la lista
        self.gestion_clientes = gestion_clientes  # Guardamos la referencia a la gestión de clientes

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        clientes = self.gestion_clientes.obtener_todos()
        #print(type(clientes), clientes)
        cliente = clientes.get(str(id_cliente))  # Convertimos id_cliente a string por seguridad
        #cliente = next((c for c in clientes if c["id"] == id_cliente), None)

        if cliente:
            mensaje = f"¿Estás seguro de que deseas eliminar al cliente '{cliente['nombre']}'?"
            vbox.Add(wx.StaticText(panel, label=mensaje), flag=wx.ALL, border=10)
            
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_ok = wx.Button(panel, wx.ID_OK, "Eliminar")
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
            hbox.Add(btn_cancel)
            
            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
            panel.SetSizer(vbox)
            
            self.Bind(wx.EVT_BUTTON, self.eliminar_cliente, btn_ok)
        else:
            wx.MessageBox(f"No se encontró el cliente con ID {id_cliente}", "Error", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL)

    def eliminar_cliente(self, event):
        try:
            self.gestion_clientes.eliminar_cliente(self.id_cliente)
            wx.MessageBox("Cliente eliminado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
            if hasattr(self.parent, "cargar_clientes"):
                self.parent.cargar_clientes()  # Actualizar la lista de clientes en la ventana principal
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
class AgregarClienteDialog(wx.Dialog):
    def __init__(self, parent, id=None, title="Nuevo Cliente"):
        super().__init__(parent, id=wx.ID_ANY, title=title)

        self.id = id  # Guarda el ID (puede ser None si es un nuevo cliente)
        self.SetTitle(title)
        # Crear el layout principal
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        grid = wx.GridBagSizer(5, 5)

        # Etiquetas y campos de entrada
        grid.Add(wx.StaticText(panel, label="Nombre:"), pos=(0, 0), flag=wx.ALL, border=5)
        self.txt_nombre = wx.TextCtrl(panel)
        grid.Add(self.txt_nombre, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(wx.StaticText(panel, label="Dirección:"), pos=(1, 0), flag=wx.ALL, border=5)
        self.txt_direccion = wx.TextCtrl(panel)
        grid.Add(self.txt_direccion, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(wx.StaticText(panel, label="Teléfono:"), pos=(2, 0), flag=wx.ALL, border=5)
        self.txt_telefono = wx.TextCtrl(panel)
        grid.Add(self.txt_telefono, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Botones
        btn_ok = wx.Button(panel, label="Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_ok.Bind(wx.EVT_BUTTON, self.guardar_cliente)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)
        # Agregar al layout
        vbox.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Centre()

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):  # Ctrl + G
            self.guardar_cliente(None)
        elif control_presionado and key_code == ord("C"):  # Ctrl + C -> Cerrar ventana
            self.Close()
        event.Skip()

    def guardar_cliente(self, event):
        nombre = self.txt_nombre.GetValue().strip()
        direccion = self.txt_direccion.GetValue().strip()
        telefono = self.txt_telefono.GetValue().strip()

        # Validación de campos obligatorios
        if not nombre or not direccion or not telefono:
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.")
            return
        # Validación del nombre
        if not re.match("^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$", nombre):
            self.mostrar_mensaje("Error: El nombre solo puede contener letras, acentos y espacios.")
            return

        # Validación del teléfono
        if not telefono.isdigit() or not (7 <= len(telefono) <= 15):
            self.mostrar_mensaje("Error: El teléfono debe contener solo números y tener entre 7 y 15 dígitos.")
            return

        # Verificar si el ID ya existe
        # Registrar cliente en el sistema (sustituye con tu lógica)
        gestion_clientes.registrar_cliente(nombre, direccion, telefono)
        print(f"Cliente guardado: Nombre={nombre}, Dirección={direccion}, Teléfono={telefono}")
        self.mostrar_mensaje("Cliente guardado con éxito.", wx.ICON_INFORMATION)

        # Limpiar campos
        self.txt_nombre.SetValue("")
        self.txt_direccion.SetValue("")
        self.txt_telefono.SetValue("")

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Información", style=tipo)

