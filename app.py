import wx
from views.fr_listProduct import ListaProductos
#from views.fr_principal import VentanaProducto

class MyApp(wx.App):
    def OnInit(self):
        self.frame = ListaProductos(None, wx.ID_ANY, "Gestión de Productos")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()