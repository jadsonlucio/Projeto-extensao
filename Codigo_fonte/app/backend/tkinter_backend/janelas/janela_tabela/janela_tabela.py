import tkinter as tk

from ....constantes import CAMINHO_JANELA_TABELA
from ...engine import ttk
from ...janelas.janela import janela

from ...frames.frames_janela_tabela.frame_tabela import frame_tabela



class janela_tabela(janela):
    def __init__(self,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.set_config(CAMINHO_JANELA_TABELA)


    def iniciar_componentes(self,**kwargs):
        self.frame_janela_tabela=frame_tabela(self,self)
        self.frame_janela_tabela.pack(expand=1,fill=tk.BOTH,anchor=tk.N)



def criar_janela_tabela(frames=None,top_level=None):
    pass