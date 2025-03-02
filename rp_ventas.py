import wx
import json
from datetime import datetime
import os

def cargar_datos_ventas(ruta_archivo):
    """Carga los datos de ventas desde un archivo JSON."""
    try:
        with open(ruta_archivo, 'r') as archivo:
            data = json.load(archivo)
        return data
    except FileNotFoundError:
        wx.MessageBox(f"Error: No se encontró el archivo {ruta_archivo}", "Error", wx.OK | wx.ICON_ERROR)
        return None
    except json.JSONDecodeError:
        wx.MessageBox(f"Error: El archivo {ruta_archivo} no contiene JSON válido", "Error", wx.OK | wx.ICON_ERROR)
        return None

def cargar_datos_productos(ruta_archivo):
    """Carga los datos de productos desde un archivo JSON."""
    try:
        with open(ruta_archivo, 'r') as archivo:
            data = json.load(archivo)
        return data
    except FileNotFoundError:
        wx.MessageBox(f"Error: No se encontró el archivo {ruta_archivo}", "Error", wx.OK | wx.ICON_ERROR)
        return None
    except json.JSONDecodeError:
        wx.MessageBox(f"Error: El archivo {ruta_archivo} no contiene JSON válido", "Error", wx.OK | wx.ICON_ERROR)
        return None

def generar_reporte_ventas(data, fecha_inicio, fecha_fin):
    """Genera un reporte de ventas filtrado por un rango de fechas."""
    reporte = []
    formato_fecha = "%d/%m/%Y %H:%M:%S"

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, formato_fecha)
        fecha_fin = datetime.strptime(fecha_fin, formato_fecha)
    except ValueError:
        return "Error: Formato de fecha incorrecto. Use DD/MM/AAAA HH:MM:SS"

    for venta in data:
        fecha_venta = datetime.strptime(venta["fecha"], formato_fecha)
        if fecha_inicio <= fecha_venta <= fecha_fin:
            reporte.append(venta)

    return reporte

class ReporteVentasFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 450))

        self.panel = wx.Panel(self)

        # Cargar datos desde el archivo ventas.json
        ruta_archivo_ventas = os.path.join("data", "ventas.json")
        self.data_ventas = cargar_datos_ventas(ruta_archivo_ventas)

        if self.data_ventas is None:
            return  # Salir si no se pudieron cargar los datos

        # Cargar datos desde el archivo productos.json
        ruta_archivo_productos = os.path.join("data", "productos.json")
        self.data_productos = cargar_datos_productos(ruta_archivo_productos)

        if self.data_productos is None:
            return  # Salir si no se pudieron cargar los datos

        # Panel con borde para las fechas
        static_box = wx.StaticBox(self.panel, label="Filtros de Fecha", pos=(10, 10), size=(300, 80))
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)

        # Controles para las fechas
        wx.StaticText(self.panel, label="Fecha de inicio:", pos=(20, 30))
        self.fecha_inicio_ctrl = wx.TextCtrl(self.panel, pos=(130, 30), value="28/02/2025 00:00:00")
        wx.StaticText(self.panel, label="Fecha de fin:", pos=(20, 60))
        self.fecha_fin_ctrl = wx.TextCtrl(self.panel, pos=(130, 60), value="01/03/2025 23:59:59")

        # Botón para generar el reporte
        self.generar_btn = wx.Button(self.panel, label="Generar reporte", pos=(320, 30))
        self.generar_btn.Bind(wx.EVT_BUTTON, self.on_generar_reporte)

        # Botón para cerrar la ventana
        self.cerrar_btn = wx.Button(self.panel, label="Cerrar", pos=(450, 30))
        self.cerrar_btn.Bind(wx.EVT_BUTTON, self.on_cerrar)

        # Área para mostrar el reporte
        self.reporte_text = wx.TextCtrl(self.panel, pos=(10, 110), size=(580, 280), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.Show(True)

    def on_generar_reporte(self, event):
        """Genera el reporte y lo muestra en el área de texto."""
        fecha_inicio = self.fecha_inicio_ctrl.GetValue()
        fecha_fin = self.fecha_fin_ctrl.GetValue()

        reporte_generado = generar_reporte_ventas(self.data_ventas, fecha_inicio, fecha_fin)

        if isinstance(reporte_generado, list):
            # Formatear el reporte como texto legible
            reporte_formateado = ""
            total_ventas = 0
            for venta in reporte_generado:
                for producto in venta['productos']:
                    id_producto = str(producto['id_producto']) # Los ids en el json de productos son string.
                    if id_producto in self.data_productos:
                        nombre_producto = self.data_productos[id_producto]['nombre']
                        precio_producto = self.data_productos[id_producto]['precio']
                        reporte_formateado += f"Fecha: {venta['fecha']}, Producto: {nombre_producto}, Cantidad: {producto['cantidad']}, Precio: {precio_producto}\n"
                        total_ventas += precio_producto * producto['cantidad']
                    else:
                        reporte_formateado += f"Fecha: {venta['fecha']}, Producto: ID {id_producto} no encontrado, Cantidad: {producto['cantidad']}, Precio: 0.0\n"
            reporte_formateado += f"\nTotal de ventas del periodo: {total_ventas}"
            self.reporte_text.SetValue(reporte_formateado)
        else:
            self.reporte_text.SetValue(reporte_generado)

    def on_cerrar(self, event):
        """Cierra la ventana."""
        self.Close(True)

if __name__ == '__main__':
    app = wx.App()
    frame = ReporteVentasFrame(None, "Reportes de Ventas")
    app.MainLoop()