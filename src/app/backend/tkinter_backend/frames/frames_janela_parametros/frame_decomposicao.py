import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento

class frame_decomposicao(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_decomposicao",container)

    def func_aplicar(self):
        try:
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()
            for serie in series_selecionadas:
                frequencia=int(serie.converter_tempo("dia",int(self.frequencia.get())))
                inst_processamento.operacoes_series.decomposicao(serie,self.box_metrica.get(),self.box_modelo.get(),frequencia)
            self.janela.destroy()
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.label_parametro=tk.Label(self,text="Selecione o parâmetro")
            self.label_parametro.pack()

            self.box_metrica=ttk.Combobox(self)
            self.box_metrica.config(justify=tk.CENTER, width=13)
            self.box_metrica.pack()
            self.box_metrica['value'] = ["Tendência","Sazonalidade","Ruído"]
            self.box_metrica['state'] = 'readonly'
            self.box_metrica.current(newindex=0)

            self.label_modelo=tk.Label(self,text="Selecione o Modelo")
            self.label_modelo.pack()

            self.box_modelo=ttk.Combobox(self)
            self.box_modelo.config(justify=tk.CENTER, width=13)
            self.box_modelo.pack()
            self.box_modelo['value'] = ["Aditivo","Multiplicativo"]
            self.box_modelo['state'] = 'readonly'
            self.box_modelo.current(newindex=0)

            self.label_frequencia = tk.Label(self, text="Digite a frequência (dias):")
            self.label_frequencia.pack()
            self.frequencia = tk.Entry(self)
            self.frequencia.pack()

            self.botao_cancelar=tk.Button(self,text="Cancelar",command=lambda:self.janela.destroy())
            self.botao_aplicar=tk.Button(self,text="Aplicar",command=self.func_aplicar)

            self.botao_cancelar.pack()
            self.botao_aplicar.pack()
        except Exception as e:
            print(str(e))

