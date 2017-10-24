import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame
from ...box import show_info

from .....processamento.series_temporais.processamento import processamento
from .....libs.regressao.OLS_model import OLS

class frame_correlacao(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_correlacao",container)

    def func_aplicar(self):
        try:
            index_serie_1=self.box_serie_1.current()
            index_serie_2=self.box_serie_2.current()
            serie_1=self.series_selecionadas[index_serie_1]
            serie_2=self.series_selecionadas[index_serie_2]
            correlacao=serie_1.correlacao(serie_2)[0][1]
            label_text="Correlação entre "+serie_1.text_legenda+" e "+serie_2.text_legenda+":"+str(round(correlacao,3))
            inst_processamento = processamento.instancia_selecionada
            inst_processamento.processamento_plot.plot_correlacao(serie_1,serie_2,label=label_text)

            model=OLS(self.series_selecionadas[:-1],self.series_selecionadas[-1],self.series_selecionadas[-1])
            model.fit_model(self.series_selecionadas[-1])
            print(model.get_informacoes()["r quadrado"])
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            inst_processamento = processamento.instancia_selecionada
            self.series_selecionadas = [serie for serie in inst_processamento.get_series_selecionadas()]
            array_series=[]
            if(len(self.series_selecionadas)<2):
                show_info("Erro","Selecione mais de 1 Série",self.janela)
                self.janela.destroy()
            else:
                for serie in self.series_selecionadas:
                    array_series.append(serie.text_legenda)

                self.text_serie_1=tk.Label(self,text="Primeira série")
                self.text_serie_1.pack()
                self.box_serie_1=ttk.Combobox(self)
                self.box_serie_1["value"]=array_series
                self.box_serie_1['state'] = 'readonly'
                self.box_serie_1.current(newindex=0)
                self.box_serie_1.pack()

                self.text_serie_2 = tk.Label(self,text="Segunda série")
                self.text_serie_2.pack()
                self.box_serie_2 = ttk.Combobox(self)
                self.box_serie_2["value"] = array_series
                self.box_serie_2['state'] = 'readonly'
                self.box_serie_2.current(newindex=1)
                self.box_serie_2.pack()

                self.botao_cancelar = tk.Button(self, text="Cancelar", command=lambda: self.janela.destroy())
                self.botao_aplicar = tk.Button(self, text="Plotar correlação", command=self.func_aplicar)
                self.botao_cancelar.pack()
                self.botao_aplicar.pack()

        except Exception as e:
            print(str(e))

