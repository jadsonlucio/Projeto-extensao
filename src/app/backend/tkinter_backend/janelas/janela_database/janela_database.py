import tkinter as tk

from ...engine import ttk
from ...janelas.janela import janela
from ...frames.frame_janela_database.frame_database import frame_database

from ....constantes import CAMINHO_JANELA_DATABASE,CAMINHO_ICON_JANELA

class janela_database(janela):
    def __init__(self,frame_inicial=None,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.set_config(CAMINHO_JANELA_DATABASE)
        self.resizable(width=True,height=True)
        self.grab_set()
        self.frame_inicial=frame_inicial

        self._iniciar_componentes()

    def _iniciar_componentes(self):
        self.iniciar_componentes()
        self.frame_add_database = frame_database(self, self.container)


    def close_window(self):
        self.frame_inicial.set_config_obj(self.frame_inicial.frame_menu,"state","enable")


