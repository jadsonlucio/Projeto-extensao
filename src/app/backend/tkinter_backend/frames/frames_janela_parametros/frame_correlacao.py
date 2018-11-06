import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame
from ...box import show_info
from ...janelas.janela_tabela.janela_tabela import janela_tabela

from .....processamento.series_temporais.processamento import processamento
from .....processamento.threading import criar_thread
from .....libs.regressao.OLS_model import OLS

class frame_correlacao(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_correlacao",container)

    def func_plot_correlacao(self):
        try:
            index_serie_1=self.box_serie_1.current()
            index_serie_2=self.box_serie_2.current()
            serie_1=self.series_selecionadas[index_serie_1]
            serie_2=self.series_selecionadas[index_serie_2]
            correlacao=serie_1.correlacao(serie_2)[0][1]
            label_text="A correlação entre "+serie_1.text_legenda+" e "+serie_2.text_legenda+" é de "+str(round(correlacao,2)*100)+"%"
            inst_processamento = processamento.instancia_selecionada
            inst_processamento.processamento_plot.plot_correlacao(serie_1,serie_2,label=label_text)
        except Exception as e:
            print(str(e))

    def func_criar_tabela_correlacao(self):
        try:

            array_informacoes=[]
            text_var = tk.StringVar()
            bar_var = tk.DoubleVar()
            self.criar_load_bar(mode='indeterminado', text_var=text_var, bar_var=bar_var)
            for cont in range(0,len(self.series_selecionadas)):
                series_treinamento=self.series_selecionadas[:]
                series_treinamento.remove(series_treinamento[cont])
                serie_treinamento=self.series_selecionadas[cont]
                model=OLS(series_treinamento,serie_treinamento)
                model.fit_model(serie_treinamento)
                informacoes=model.get_informacoes()
                if(cont==0):
                    array_informacoes.append(informacoes.keys())
                array_informacoes.append(informacoes.values())

            self.loadbar.hide_load()

            self.janena_tabela=janela_tabela(None,self.janela)
            self.janena_tabela.iniciar_componentes()
            self.janena_tabela.frame_janela_tabela.tabela.criar_tabela("Correlacões")
            self.janena_tabela.frame_janela_tabela.set_tabela_data(0,array_informacoes)
            self.janena_tabela.frame_janela_tabela.iniciar_componentes()
        except Exception as e:
            print(str(e))

    def run_func_aplicar(self):
        try:
            thread=criar_thread(self.func_criar_tabela_correlacao)
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

                self.text_serie_1=tk.Label(self,text="Série primária")
                self.text_serie_1.pack()
                self.box_serie_1=ttk.Combobox(self)
                self.box_serie_1["value"]=array_series
                self.box_serie_1['state'] = 'readonly'
                self.box_serie_1.current(newindex=0)
                self.box_serie_1.pack()

                self.text_serie_2 = tk.Label(self,text="Série secundária")
                self.text_serie_2.pack()
                self.box_serie_2 = ttk.Combobox(self)
                self.box_serie_2["value"] = array_series
                self.box_serie_2['state'] = 'readonly'
                self.box_serie_2.current(newindex=1)
                self.box_serie_2.pack()

                self.botao_plot_correlacao = tk.Button(self, text="Plotar correlação", command=self.func_plot_correlacao)
                self.botao_plot_correlacao.pack(anchor=tk.E)

                self.botao_criar_tabela=tk.Button(self,text="Tabela de correlacão múltipla",command=self.run_func_aplicar)
                self.botao_criar_tabela.pack()
        except Exception as e:
            print(str(e))

