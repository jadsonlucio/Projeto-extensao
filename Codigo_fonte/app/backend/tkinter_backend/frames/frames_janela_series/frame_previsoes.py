import tkinter as tk
from ...engine import ttk,Frame
from ...load import load_icons
from ...frames.frame import frame,frame_container
from ...box import opendirectory,openfiles
from ...objetos import frame_scroll,frame_objetos_list,date_choice
from ....constantes import CAMINHO_ICONS_FRAME_SERIES

from .....processamento.previsao_series.previsao import array_previsao,previsao,load_previsao
from .....processamento.threading import criar_thread


class frame_container_previsoes(frame_container):
    def __init__(self,janela,container):
        frame_container.__init__(self,janela,'frame_container_previsoes',container)
        self.iniciar_componentes()

    def iniciar_componentes(self):
        try:
            self.titles=['frame_previsoes']
            self.frame_series=frame_previsoes(self.janela,self)
            self.frame_series.iniciar_componentes()
            self.frame_criar_previsao=frame_criar_previsao(self.janela,self)
            self.frame_criar_previsao.iniciar_componentes()
            self.frame_previsao=frame_previsao(self)
            self.frame_previsao.iniciar_componentes()
            self.add_frame(self.frame_series,"frame_previsoes")
            self.add_frame(self.frame_criar_previsao, "frame_criar_previsao")
            self.add_frame(self.frame_previsao,"frame_previsao")
            self.show_frame("frame_previsoes")
        except Exception as e:
            print(str(e))

class frame_previsoes(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_previsoes",container)
        self.icones = load_icons(CAMINHO_ICONS_FRAME_SERIES, ".png")

    def iniciar_componentes(self):
        try:
            self.frame_previsoes=frame_objetos_list(self,None,self.selecionar_previsao,None,270,50,1)
            self.frame_previsoes.pack(fill=tk.BOTH,expand=1)

            self.barra_opcoes=tk.Frame(self,height=30)
            self.barra_opcoes.pack(side=tk.TOP,fill=tk.X)

            self.botao_add=tk.Button(self.barra_opcoes,command=self.criar_previsao)
            self.botao_add.config(image=self.icones["create_obj"],relief=tk.FLAT)
            self.botao_add.image=self.icones["create_obj"]
            self.botao_add.pack(side=tk.LEFT)

            self.botao_open = tk.Button(self.barra_opcoes,command=self.abrir_previsao)
            self.botao_open.config(image=self.icones["open"],relief=tk.FLAT)
            self.botao_open.image = self.icones["open"]
            self.botao_open.pack(side=tk.LEFT)

            self.botao_save = tk.Button(self.barra_opcoes,command=self.salvar_previsao)
            self.botao_save.config(image=self.icones["save"], relief=tk.FLAT)
            self.botao_save.image = self.icones["save"]
            self.botao_save.pack(side=tk.LEFT)

            self.load_previsoes(array_previsao)

        except Exception as e:
            print(str(e))

    def criar_previsao(self):
        try:
            self.container.show_frame("frame_criar_previsao")
        except Exception as e:
            print(str(e))

    def salvar_previsao(self):
        try:
            self.botao_save["state"]="disabled"
            url_diretorio=opendirectory()
            for previsao in self.frame_previsoes.get_selected_obj():
                previsao.save(url_diretorio)
            self.botao_save["state"] = "normal"
        except Exception as e:
            self.botao_save["state"] = "normal"
            print(str(e))

    def abrir_previsao(self):
        try:
            self.botao_open["state"]="disabled"
            filetypes = (("Previsão(.prev)", "*.prev"), ("Previsão(.previsao)", "*.st*"))
            arquivo_info_previsao = openfiles(filetypes=filetypes)[0]
            load_previsao(arquivo_info_previsao)
            self.load_previsoes(array_previsao)
            self.botao_open["state"] = "normal"
        except Exception as e:
            self.botao_open["state"] = "normal"
            print(str(e))

    def load_previsoes(self,previsoes):
        try:
            self.frame_previsoes.clear_frame_widgets()
            for previsao in previsoes:
                self.frame_previsoes.add_objeto(previsao,previsao.tipo_previsao,False)
        except Exception as e:
            print(str(e))

    def selecionar_previsao(self,previsao):
        try:
            self.container.get_frame("frame_previsao").load_previsao(previsao)
            self.container.show_frame("frame_previsao")
        except Exception as e:
            print(str(e))

class frame_criar_previsao(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_criar_previsao",container)
        self.janela=janela
        self.set_config()

    def importar_series(self,frame_objetos_list):
        try:
            series_selecionadas=self.janela.frame_container_series.frame_series.get_selected_series()
            for serie in series_selecionadas:
                frame_objetos_list.add_objeto(serie,serie.text_legenda,True)
        except Exception as e:
            print(str(e))

    def selecionar_serie(self,serie):
        pass

    def criar_previsao(self):
        try:
            tipo_previsao=self.tipo_previsao.get()
            if(tipo_previsao=="Rede neural"):
                prev=previsao(tipo_previsao,None,self.frame_series_treinamento.get_selected_obj(),self.frame_series_previsao.objetos,self.frame_series_previsao.get_selected_obj())
            else:
                prev = previsao(tipo_previsao, None, self.frame_series_treinamento.get_selected_obj(),self.frame_series_previsao.get_selected_obj())
            self.container.frame_series.load_previsoes(array_previsao)
            self.container.show_frame("frame_previsoes")
        except Exception as e:
            print(str(e))


    def voltar_janela_previsoes(self):
        try:
            self.container.show_frame("frame_previsoes")
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.text_tipo_previsao=tk.Label(self,text="Selecione o método de previsão:")
            self.text_tipo_previsao.pack(anchor=tk.NW)

            self.tipo_previsao=ttk.Combobox(self)
            self.tipo_previsao["value"]=["Holt-winters Aditivo","Holt-winters Multiplicativo","Holt-winters Linear","Regressão","Rede neural"]
            self.tipo_previsao['state'] = 'readonly'
            self.tipo_previsao.current(newindex=0)
            self.tipo_previsao.pack(anchor=tk.NW)

            self.text_series_treinamento=tk.Label(self,text="Escolha as séries de treinamento:")
            self.text_series_treinamento.pack(anchor=tk.NW)

            self.frame_series_treinamento=frame_objetos_list(self,None,self.selecionar_serie,None,85,30,3)
            self.frame_series_treinamento.config(width=280,height=85)
            self.frame_series_treinamento.pack_propagate(False)
            self.frame_series_treinamento.pack()

            self.botao_importar_series_treinamento=ttk.Button(self,text="Importar séries selecionadas",
                                                   command=lambda:self.importar_series(self.frame_series_treinamento))
            self.botao_importar_series_treinamento.pack(anchor=tk.NE)

            self.text_series_previsao = tk.Label(self, text="Escolha as séries de previsao:")
            self.text_series_previsao.pack(anchor=tk.NW)

            self.frame_series_previsao = frame_objetos_list(self,None,self.selecionar_serie, None, 85, 30, 3)
            self.frame_series_previsao.config(width=280, height=85)
            self.frame_series_previsao.pack_propagate(False)
            self.frame_series_previsao.pack()

            self.botao_importar_series_previsao = ttk.Button(self, text="Importar séries selecionadas",
                                                               command=lambda: self.importar_series(
                                                                   self.frame_series_previsao))
            self.botao_importar_series_previsao.pack(anchor=tk.NE)

            self.frames_botoes=tk.Frame(self)
            self.frames_botoes.pack(anchor=tk.SW)

            self.botao_voltar = ttk.Button(self.frames_botoes, text="Voltar", command=self.voltar_janela_previsoes)
            self.botao_voltar.pack(side=tk.LEFT,padx=10,pady=2)

            self.botao_criar_previsao=ttk.Button(self.frames_botoes,text="Criar previsão",command=self.criar_previsao)
            self.botao_criar_previsao.pack(side=tk.LEFT,pady=2)

        except Exception as e:
            print(str(e))


class frame_previsao(Frame):
    def __init__(self,container):
        Frame.__init__(self,container)

    def iniciar_componentes(self):
        self.botao_prever = tk.Button(self,command=self.prever)
        self.botao_prever.place(relx=0.03, rely=0.08, height=84, width=117)
        self.botao_prever.configure(pady="0")
        self.botao_prever.configure(text='''Prever''')
        self.botao_prever.configure(width=117)

        self.botao_treinar = tk.Button(self,command=lambda:self.fit_previsao(None))
        self.botao_treinar.place(relx=0.58, rely=0.08, height=84, width=117)
        self.botao_treinar.configure(pady="0")
        self.botao_treinar.configure(text='''Treinar''')

        self.frame_prever = ttk.LabelFrame(self)
        self.frame_prever.place(relx=0.03, rely=0.36, relheight=0.45
                                , relwidth=0.93)
        self.frame_prever.configure(relief=tk.GROOVE)
        self.frame_prever.configure(text='''Prever''')
        self.frame_prever.configure(width=285)

        self.metrica = ttk.Combobox(self.frame_prever)
        self.metrica.place(relx=0.04, rely=0.26, relheight=0.2, relwidth=0.9)
        self.metrica["state"]='readonly'
        self.metrica.configure(takefocus="")

        self.text_metrica_treinamento = tk.Label(self.frame_prever)
        self.text_metrica_treinamento.place(relx=0.04, rely=0.009, height=31
                                            , width=254)
        self.text_metrica_treinamento.configure(text='''Selecione a métrica para previsão''')

        self.text_data_treinamento = tk.Label(self.frame_prever)
        self.text_data_treinamento.place(relx=0.04, rely=0.5, height=31
                , width=254)
        self.text_data_treinamento.configure(text='''Selecione a data para previsão''')

        self.data_choice=tk.Entry(self.frame_prever)
        self.data_choice.place(relx=0.04, rely=0.7, relheight=0.2, relwidth=0.9)

    def load_previsao(self,previsao):
        try:
            self.previsao=previsao
            self.array_metricas=[]
            for serie in  self.previsao.model.series_previsao:
                self.array_metricas.append(serie.text_legenda)
            self.metrica["value"]=self.array_metricas
            self.metrica.current(0)
            if(not previsao.model.model_fited):
                self.botao_prever.config(state="disabled")
                self.text_data_treinamento.config(state="disabled")
                self.text_metrica_treinamento.config(state="disabled")
        except Exception as e:
            print(str(e))


    def fit_previsao(self,previsao=None):
        try:
            def run():
                try:
                    self.botao_treinar["state"]="disabled"
                    self.barra_progresso=ttk.Progressbar(self,length=300, mode='determinate')
                    self.barra_progresso.start(25)
                    self.barra_progresso.place(relx=0.04, rely=0.86, relheight=0.2, relwidth=0.9)
                    print(self.previsao.model)
                    self.previsao.model.fit_model(self.previsao.model.serie_treinamento)
                    self.barra_progresso.destroy()
                    self.botao_prever.config(state="normal")
                    self.text_data_treinamento.config(state="normal")
                    self.text_metrica_treinamento.config(state="normal")
                except Exception as e:
                    self.botao_treinar["state"] = "normal"

            if(previsao!=None):
                self.previsao=previsao
            criar_thread(run)
        except Exception as e:
            print(str(e))

    def prever(self,previsao=None):
        try:
            index_serie_previsao=int(self.metrica.current())
            serie_prevista=self.previsao.prever_serie(index_serie_previsao,self.data_choice.get())
            serie_prevista.plot(label=serie_prevista.text_legenda,plot_date=True)
        except Exception as e:
            print(str(e))
