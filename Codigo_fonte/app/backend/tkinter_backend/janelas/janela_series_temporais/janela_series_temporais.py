import tkinter as tk
from ....constantes import CAMINHO_JANELA_SERIES
from ...engine import ttk
from ...janelas.janela import janela
from ...frames.frames_janela_series.frame_series import frame_container_series
from ...frames.frames_janela_series.frame_previsoes import frame_container_previsoes
from ...frames.frames_janela_estatisticas.frame_estatisticas import frame_estatisticas

class janela_series_temporais(janela):

    #gets e sets

    def get_frame_notebook(self,index):
        try:
            if(isinstance(index,str)):
                return self.notebook_frames[index]
            else:
                raise ValueError("Index não encontrado")
        except Exception as e:
            print(str(e))

    def __init__(self,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.set_config(CAMINHO_JANELA_SERIES)
        self.wm_attributes("-topmost",1)
        self.wm_attributes("-toolwindow",1)
        self.resizable(width=False,height=False)
        self.notebook_frames={}
        self.iniciar_componentes()

    def add_notebook_frame(self,frame,text):
        try:
            self.notebook.add(frame,text=text)
            self.notebook_frames[text]=frame
        except Exception as e:
            print(str(e))

    def show_notebook_frame(self,index):
        try:
            if(isinstance(index,str)):
                if (isinstance(index, str)):
                    self.notebook.select(self.notebook_frames[index])
                else:
                    raise ValueError("Index não encontrado")
        except Exception as e:
            print(str(e))

    def hide_notebook_frame(self,index):
        try:
            if(isinstance(index,str)):
                if (isinstance(index, str)):
                    self.notebook.hide(self.notebook_frames[index])
                else:
                    raise ValueError("Index não encontrado")
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.notebook=ttk.Notebook(self)
            self.notebook.pack(fill=tk.BOTH,expand=True)
            self.frame_container_series=frame_container_series(self,self)
            self.frame_previsoes_series=frame_container_previsoes(self,self)
            self.frame_estatisticas=frame_estatisticas(self,self)

            self.add_notebook_frame(self.frame_container_series,"Séries temporais")
            self.add_notebook_frame(self.frame_previsoes_series,"Previsões")
            self.add_notebook_frame(self.frame_estatisticas,"Estatísticas")

            self.hide_notebook_frame("Estatísticas")
        except Exception as e:
            print(str(e))
