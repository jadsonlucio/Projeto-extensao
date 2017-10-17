import tkinter as tk
from ...engine import ttk,Frame

from ...frames.frame import frame
from ...box import opendirectory
from ...objetos import frame_scroll,frame_informacoes
from .....processamento.estatistica_serie import estatisticas_series

class frame_estatisticas(frame):

    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_estatisticas",container)
        self.iniciar_componentes()
        self.frames_estatistica={}

    def load_estatistica(self,index):
        try:
            if(isinstance(index,int)):
                estatistica=estatisticas_series[index]
            else:
                estatistica=index
            self.frame_scroll.clear_frame_widgets()
            self.current_estatistica=estatistica
            self.var_text_serie.set(self.current_estatistica.serie_temporal.text_legenda)
            self.frame_estatistica=frame_estatistica(self.frame_scroll.frame_widgets,self.current_estatistica)
            self.frame_estatistica.iniciar_componentes()
            self.frame_estatistica.config(width=280,height=230)
            self.frame_estatistica.pack()
        except Exception as e:
            print(str(e))

    def save_estatisticas(self):
        try:
            url_arquivo=opendirectory()
            self.current_estatistica.salvar_estatistica(url_arquivo)
        except Exception as e:
            print(str(e))

    def fechar_frame(self):
        try:
            self.janela.hide_notebook_frame("Estatísticas")
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.var_text_serie=tk.StringVar()
            self.text_serie_legenda=tk.Label(self,textvariable=self.var_text_serie)
            self.text_serie_legenda.pack(fill=tk.X)
            self.text_serie_legenda.config(background="gainsboro")

            self.botao_fechar=ttk.Button(self,text="x",width=2,command=self.fechar_frame)
            self.botao_fechar.pack(anchor=tk.SE)

            self.frame_scroll=frame_scroll(self)
            self.frame_scroll.pack(fill=tk.BOTH,expand=1)
            self.frame_scroll.iniciar_componentes()

            self.botao_salvar_estatistica=tk.Button(self,text="Salvar Estatísticas",command=self.save_estatisticas)
            self.botao_salvar_estatistica.pack()

        except Exception as e:
            print(str(e))


class frame_estatistica(Frame):
    def __init__(self,container,estatistica_serie):
        Frame.__init__(self,container)
        self.estatistica_serie=estatistica_serie

    def iniciar_componentes(self):
        try:
            self.estatistica_serie.set_estatisticas()
            self.frame_info = frame_informacoes(self, 3, self.estatistica_serie.estatisticas)
            self.frame_info.create_frames()
            self.frame_info.config(width=275,height=225)
            self.frame_info.pack()
        except Exception as e:
            print(str(e))

