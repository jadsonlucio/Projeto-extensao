import tkinter as tk

from ....constantes import CAMINHO_JANELA_TABELA
from ...engine import ttk
from ...janelas.janela import janela

from ...frames.frames_janela_tabela.frame_tabela import frame_tabela



class janela_tabela(janela):
    def __init__(self,frames=None,top_level=None,set_config=True):
        janela.__init__(self,top_level,frames)
        if(set_config):
            self.set_config(CAMINHO_JANELA_TABELA)


    def iniciar_componentes(self,**kwargs):
        self.frame_div_opcoes=tk.Frame(self)
        self.frame_div_opcoes.config(width=30,background="whitesmoke")
        self.frame_div_opcoes.pack(anchor=tk.NW)

        self.frame_janela_opcoes=tk.Frame(self)
        self.frame_janela_opcoes.pack(anchor=tk.NW)

        self.frame_janela_tabela=frame_tabela(self,self)
        self.frame_janela_tabela.pack(expand=1,fill=tk.BOTH,anchor=tk.N)



def criar_janela_tabela(frames=None,top_level=None):
    pass