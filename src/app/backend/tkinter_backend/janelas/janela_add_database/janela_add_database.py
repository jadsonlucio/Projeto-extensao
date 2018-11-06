import tkinter as tk

from ...engine import ttk
from ...janelas.janela import janela
from ...frames.frame_janela_add_database.frame_add_database import frame_add_database

from ....constantes import CAMINHO_JANELA_ADD_DATABASE,CAMINHO_ICON_JANELA

class janela_add_database(janela):
    def __init__(self,frame_inicial=None,frame_database=None,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.set_config(CAMINHO_JANELA_ADD_DATABASE)
        self.resizable(width=False,height=False)
        self.frame_inicial=frame_inicial
        self.frame_database=frame_database
        self.grab_set()

        self._iniciar_componentes()

    def _iniciar_componentes(self):
        self.iniciar_componentes()
        self.frame_add_database=frame_add_database(self,self.container)


    def close_window(self):
        if(self.frame_inicial!=None):
            frame_inicial=self.frame_inicial
            frame_inicial.set_config_obj(frame_inicial.frame_erro,"state","enable")
