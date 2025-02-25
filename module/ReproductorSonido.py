import wx.adv  # Necesario para wx.adv.Sound

class ReproductorSonido:
    """Clase para gestionar la reproducción de sonidos en la aplicación."""

    @staticmethod
    def reproducir(archivo):
        """Reproduce un archivo de sonido .wav si es válido."""
        try:
            sonido = wx.adv.Sound(archivo)
            if sonido.IsOk():
                sonido.Play(wx.adv.SOUND_ASYNC)  # Reproduce sin bloquear la app
            else:
                print(f"Error: No se pudo cargar el archivo de sonido '{archivo}'.")
        except Exception as e:
            print(f"Error al reproducir sonido: {e}")



