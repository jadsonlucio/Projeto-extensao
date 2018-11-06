import tkinter as tk

from ....constantes import CAMINHO_JANELA_ESTATISTICAS
from ...engine import ttk
from ...janelas.janela import janela
from ...frames.frames_janela_estatisticas import frame_estatisticas


class janela_estatisticas(janela):
    def __init__(self,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.set_config(CAMINHO_JANELA_ESTATISTICAS)
        self.iniciar_componentes()

    def iniciar_componentes(self):
        try:
            self.frame_estatisticas=frame_estatisticas.frame_estatisticas(self,self)
            self.frame_estatisticas.pack(fill=tk.BOTH,expand=1)
        except Exception as e:
            print(str(e))

