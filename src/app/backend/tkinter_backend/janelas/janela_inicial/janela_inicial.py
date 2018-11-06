from ...janelas.janela import janela
from ....constantes import CAMINHO_JANELA_INICIAL,CAMINHO_ICON_JANELA

class janela_inicial(janela):
    def __init__(self,frames,top_level=None):
        janela.__init__(self,top_level,frames)
        self.minsize(1000,678)
        self.maximize()
        self.set_config(CAMINHO_JANELA_INICIAL)
