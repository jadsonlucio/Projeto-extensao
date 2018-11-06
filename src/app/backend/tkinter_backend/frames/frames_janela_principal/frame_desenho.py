import tkinter as tk
from ...engine import ttk
from ...janelas import janela_series_temporais
from ...janelas import janela_parametros
from ...box import _show_error
from ...objetos import date_choice
from ..frame import frame
from ..frames_janela_principal.frame_grafico import frame_plot,frame_grafico

from .....instancias.Instancias import get_instancia
from .....processamento.series_temporais.processamento import processamento

class frame_desenho(frame):
    def __init__(self, janela, container):
        frame.__init__(self, janela, 'frame_desenho', container)
        self.janela = janela
        self.container=container
        self.set_config()
        self.iniciar_componentes()

    #funcões criacao

    def iniciar_componentes(self):
        self.frame_estatisticas = frame_estatisticas(self.janela, self)
        self.frame_grafico = frame_grafico(self.janela, self)
        self.frame_opcoes = frame_opcoes(self.janela, self)

class frame_opcoes(frame):

    #geters e seters

    def set_value_metricabox(self, array=None):
        try:
            if(array==None):
                self.metrica_box['values']=get_instancia("pre_processamento").keys_array
            else:
                self.metrica_box['value']=array
            self.metrica_box.current(newindex=0)
        except Exception as e:
            print(str(e))

    def __init__(self, janela, container):
        frame.__init__(self, janela, 'frame_opcoes', container)
        self.container=container
        self.janela = janela
        self.iniciar_componentes()

    #funcões plotagem

    def plot_normal(self):
        try:
            data_inicial = self.data_inicial.get_data()
            data_final = self.data_final.get_data()
            text_legenda=self.metrica_box.get()
            index = self.metrica_box.current()
            if(data_inicial<data_final):
                processamento = frame_plot.instancia_selecionada.processamento
                data_x, data_y = processamento._get_serie_data(data_inicial, data_final, index)
                periodo=processamento.pre_processamento.periodo
                time_steps=processamento.pre_processamento.time_steps
                serie = processamento._criar_serie_temporal(data_x, data_y, data_inicial, data_final, periodo, time_steps,text_legenda,None,
                                                            'Normal')

                serie.plot(label=text_legenda,plot_date=True)
        except Exception as e:
            print(str(e))

    #funcões criação

    def iniciar_componentes(self):
        try:
            self.config(width=175)
            self.pack(fill=tk.BOTH, side=tk.LEFT)
            self.pack_propagate(False)
            self.text_metrica = tk.Label(self, text="Selecione a métrica")
            self.text_metrica.config(background="gainsboro", foreground="black", font="Arial 10 bold")
            self.text_metrica.pack(anchor=tk.CENTER, pady=2)

            self.metrica_box = ttk.Combobox(self)
            self.metrica_box.config(justify=tk.CENTER, width=13)
            self.metrica_box.pack(pady=2)
            self.metricas_text = []

            self.metrica_box['value'] = get_instancia("pre_processamento").keys_array
            self.metrica_box['state'] = 'readonly'
            self.metrica_box.current(newindex=0)

            self.div1 = tk.Frame(self, height=8, background="gainsboro")
            self.div1.pack_propagate(False)
            self.div1.pack(fill=tk.X)

            self.text_data_inicio = tk.Label(self, text="Data inicial")
            self.text_data_inicio.config(background="gainsboro", foreground="black", font="Arial 10 bold")
            self.text_data_inicio.pack(pady=2)

            self.data_inicial = date_choice(self)
            self.data_inicial.iniciar_componentes(2013, 2020)
            self.data_inicial.pack()

            self.div2 = tk.Frame(self, height=10, background="gainsboro")
            self.div2.pack_propagate(False)
            self.div2.pack(fill=tk.X)

            self.text_data_fim = tk.Label(self, text="Data final")
            self.text_data_fim.config(background="gainsboro", foreground="black", font="Arial 10 bold")
            self.text_data_fim.pack(pady=2)

            self.data_final = date_choice(self)
            self.data_final.iniciar_componentes(2013, 2020)
            self.data_final.pack()

            self.div3 = tk.Frame(self, height=10, background="gainsboro")
            self.div3.pack_propagate(False)
            self.div3.pack(fill=tk.X)

            self.botao_ok = ttk.Button(self, text="Plotar gráfico", command=self.plot_normal)
            self.botao_ok.pack(pady=2)

            self.more_options = ttk.Button(self, text="Mais opções", command=self.open_series_window)
            self.more_options.pack(pady=2)

            self.set_config()
        except Exception as e:
            print(str(e))

    def open_series_window(self):
        try:
            janela_series_temporais.janela_series_temporais.janela_series_temporais(top_level=self.janela)
        except Exception as e:
            print(str(e))

class frame_estatisticas(tk.LabelFrame):
    def __init__(self, janela, container):
        tk.LabelFrame.__init__(self, container)
        self.janela = janela
        self.container=container
        self.iniciar_componentes()

    #funcões criação

    def iniciar_componentes(self):
        try:
            self.config(text="Navegação", width=200, background='gainsboro')
            self.pack_propagate(False)
            self.pack(fill=tk.BOTH, side=tk.LEFT)

            self.text_volta_inicio = ttk.Label(self, text="<<Janela Inicial", font=("Arial", "10"))
            self.text_volta_inicio.pack(anchor=tk.W, pady=10)
            self.text_volta_inicio.bind('<Button-1>', self.voltar_telainicial)
            self.text_volta_inicio.config(foreground="black", background="gainsboro")

            self.opcoes_indicadores_estatisticas = ["Regressão Linear", "Média Móvel Simples" , "Variação",
                                                    "Média Móvel Exponencial","Decomposição da Série","Boxplot"]
            self.opcoes_indicadores_funcoes = ["Normalizar Série","Gráfico de Médias","Autocorrelação", "Correlação","Histograma"]
            self.opcoes_indicadoes_graficos=[]

            self.frame_estatistiscas = tk.Frame(self)
            self.frame_estatistiscas.pack()

            self.tree_estatisticas = ttk.Treeview(self.frame_estatistiscas, selectmode='browse', height=14)
            self.tree_estatisticas.pack(side=tk.LEFT, fill=tk.Y)
            self.tree_indicadores = self.tree_estatisticas.insert("", "end", text="Indicadores")
            self.tree_funcoes = self.tree_estatisticas.insert("", "end", text="Funções")

            for opc in self.opcoes_indicadores_estatisticas:
                obj = self.tree_estatisticas.insert(self.tree_indicadores, "end", text=opc)
            for opc in self.opcoes_indicadores_funcoes:
                obj = self.tree_estatisticas.insert(self.tree_funcoes, "end", text=opc)
                # self.treescrollbar=ttk.Scrollbar(self.frame_estatistiscas, orient="vertical",command=self.tree_estatisticas.yview)
            # self.treescrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            # self.tree_estatisticas.configure(yscrollcommand=self.treescrollbar.set)

            self.tree_estatisticas.bind("<Double-1>", self.tree_click)
            self.tree_estatisticas.item(self.tree_indicadores, open=True)
            self.tree_estatisticas.item(self.tree_funcoes, open=True)

        except Exception as e:
            print(str(e))

    def tree_click(self,event=None):
        try:
            item = self.tree_estatisticas.focus()
            text = self.tree_estatisticas.item(item)["text"]
            if(text=="Regressão Linear"):
                inst_processamento=processamento.instancia_selecionada
                series_selecionadas=inst_processamento.get_series_selecionadas()
                for serie in series_selecionadas:
                    inst_processamento.operacoes_series.regressao_linear(serie)
            if(text=="Média Móvel Simples"):
                janela_para=janela_parametros.janela_parametros.janela_parametros(frames=None,top_level=self.janela)
                janela_para.iniciar_componentes("MMS")
            if(text=="Variação"):
                inst_processamento=processamento.instancia_selecionada
                series_selecionadas=inst_processamento.get_series_selecionadas()
                for serie in series_selecionadas:
                    inst_processamento.operacoes_series.variacao(serie)
            if(text=="Média Móvel Exponencial"):
                janela_para=janela_parametros.janela_parametros.janela_parametros(frames=None,top_level=self.janela)
                janela_para.iniciar_componentes("MME")
            if(text=="Boxplot"):
                janela_para=janela_parametros.janela_parametros.janela_parametros(frames=None,top_level=self.janela)
                janela_para.iniciar_componentes("BOXPLOT")

            if(text=="Decomposição da Série"):
                janela_para=janela_parametros.janela_parametros.janela_parametros(frames=None,top_level=self.janela)
                janela_para.iniciar_componentes("DECOMPOSICAO")

            if(text=="Normalizar Série"):
                janela_para=janela_parametros.janela_parametros.janela_parametros(frames=None,top_level=self.janela)
                janela_para.iniciar_componentes("NORMALIZAR")

            if(text=="Gráfico de Médias"):
                janela_para=janela_parametros.janela_parametros.janela_parametros(frames=None,top_level=self.janela)
                janela_para.iniciar_componentes("MEDIAS")

            if(text=="Autocorrelação"):
                janela_para = janela_parametros.janela_parametros.janela_parametros(frames=None, top_level=self.janela)
                janela_para.iniciar_componentes("AUTOCORRELACAO")

            if(text=="Correlação"):
                janela_para = janela_parametros.janela_parametros.janela_parametros(frames=None, top_level=self.janela)
                janela_para.iniciar_componentes("CORRELACAO")

            if(text=="Histograma"):
                janela_para = janela_parametros.janela_parametros.janela_parametros(frames=None, top_level=self.janela)
                janela_para.iniciar_componentes("HISTOGRAMA")

        except Exception as e:
            print(str(e))

    #funcao voltar

    def voltar_telainicial(self, event):
        self.janela.show_frame('frame_inicial')

    #funcao criar janela

    def criar_janela_previsao(self):
        pass
