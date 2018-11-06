import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento

class frame_media_movel(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_media_movel",container)

    def func_aplicar(self):
        try:
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()
            for serie in series_selecionadas:
                inst_processamento.operacoes_series.media_movel_simples(serie,int(self.lag.get()))
            self.janela.destroy()
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        self.label_lag=tk.Label(self,text="Digite o lag")
        self.lag=tk.Entry(self)
        self.botao_cancelar=tk.Button(self,text="Cancelar",command=lambda:self.janela.destroy())
        self.botao_aplicar=tk.Button(self,text="Aplicar",command=self.func_aplicar)
        self.label_lag.pack()
        self.lag.pack()
        self.botao_cancelar.pack()
        self.botao_aplicar.pack()

