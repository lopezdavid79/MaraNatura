import wx


from Views.fr_menu import Principal 
#from Views.fr_listSale import ListSale as Principal
#from Views.fr_listClient import ListaClientes as Principal  
class MyApp(wx.App):
    def OnInit(self):
        self.frame = Principal(None, title="My App")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
