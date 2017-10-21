import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento

class frame_autocorrelacao(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_autocorrelacao",container)

    def func_aplicar(self):
        try:
            tipo_plote=self.box_tipo_correlacao.get()
            lag=self.lag.get()
            if(tipo_plote=="acf"):
                titulo="Autocorrelação"
            elif(tipo_plote=="pacf"):
                titulo="Autocorrelação Parcial"
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()
            if(len(series_selecionadas)==1):
                titulo=titulo+" "+series_selecionadas[0].text_legenda
                inst_processamento.processamento_plot.plot_autocorrelacao(series_selecionadas[0],tipo_plote,titulo,0.05,lag)
            elif(len(series_selecionadas)>1):
                print("Apenas 1 serie deve ser selecionada")
            else:
                print("Nenhuma serie selecionada")
            self.janela.destroy()
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.text_tipo_correlacao=tk.Label(self,text="Tipo de autocorrelação")
            self.text_tipo_correlacao.pack()
            self.box_tipo_correlacao=ttk.Combobox(self)
            self.box_tipo_correlacao["value"]=["pacf","acf"]
            self.box_tipo_correlacao['state'] = 'readonly'
            self.box_tipo_correlacao.current(newindex=0)
            self.box_tipo_correlacao.pack()

            self.label_lag = tk.Label(self, text="Digite o lag")
            self.lag = tk.Entry(self)
            self.label_lag.pack()
            self.lag.pack()

            self.botao_cancelar = tk.Button(self, text="Cancelar", command=lambda: self.janela.destroy())
            self.botao_aplicar = tk.Button(self, text="Aplicar", command=self.func_aplicar)
            self.botao_cancelar.pack()
            self.botao_aplicar.pack()
        except Exception as e:
            print(str(e))

