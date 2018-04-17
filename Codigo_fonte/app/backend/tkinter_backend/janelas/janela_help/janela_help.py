import tkinter as tk
from tkinter import ttk

from ...janelas.janela import janela
from ...frames.frames_janela_help.frame_janela_help import frame_janela_help
from ....constantes import CAMINHO_JANELA_HELP

class janela_help(janela):
    def __init__(self,dirt_functions,top_level=None,frames=None):
        janela.__init__(self,top_level,frames)
        self.resizable(0,0)
        self.set_config(CAMINHO_JANELA_HELP)
        self.iniciar_componentes(dirt_functions)

    def iniciar_componentes(self,dirt_functions):
        self.frames_principal=frame_janela_help(self,self,dirt_functions)
        self.frames_principal.iniciar_componentes()
        self.frames_principal.pack(fill=tk.BOTH,expand=1)