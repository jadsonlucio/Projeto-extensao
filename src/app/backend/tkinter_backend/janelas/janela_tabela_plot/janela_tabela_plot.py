import tkinter as tk

from ....constantes import CAMINHO_JANELA_TABELA_PLOT
from ...engine import ttk
from ...janelas.janela import janela

from ...frames.frames_janela_tabela_plot.frame_tabela_plot import frame_tabela_plot





class janela_tabela_plot(janela):
    def __init__(self,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.set_config(CAMINHO_JANELA_TABELA_PLOT)


    def iniciar_componentes(self,**kwargs):
        self.frame_tabela_plot=frame_tabela_plot(self,self)
        self.frame_tabela_plot.iniciar_componentes()
        self.frame_tabela_plot.pack(fill=tk.BOTH,expand=1)


def criar_janela_tabela(frames=None,top_level=None):
    pass