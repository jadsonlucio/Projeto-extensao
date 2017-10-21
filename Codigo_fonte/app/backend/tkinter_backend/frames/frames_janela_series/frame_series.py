import tkinter as tk
from ...load import load_icons
from ...box import openfiles,opendirectory
from ...frames.frame import frame,frame_container
from ...janelas.janela_estatisticas.janela_estatisticas import janela_estatisticas
from ...janelas.janela_tabela.janela_tabela import janela_tabela
from ...objetos import frame_scroll,frame_objetos_list,frame_informacoes,frame_code_text,frame_code_result
from ....constantes import CAMINHO_ICONS_FRAME_SERIES,CAMINHO_ICONS_FRAME_CODE


from .....processamento.series_temporais.processamento import instancias_processamento,processamento
from .....processamento.coding.coding import decode_code,run_code
from .....processamento.estatistica_serie import criar_estatistica

class frame_container_series(frame_container):
    def __init__(self,janela,container):
        frame_container.__init__(self,janela,'frame_container_series',container)
        self.iniciar_componentes()

    def iniciar_componentes(self):
        try:
            self.titles=['frame_series']
            self.frame_series=frame_series(self.janela,self)
            self.frame_series.iniciar_componentes()

            self.frame_info_serie = frame_info_serie(self.janela, self)
            self.frame_info_serie.iniciar_componentes()

            self.frame_code=frame_code(self.janela,self)
            self.frame_code.iniciar_componentes()

            self.add_frame(self.frame_info_serie, "frame_info_serie")
            self.add_frame(self.frame_series,"frame_series")
            self.add_frame(self.frame_code,"frame_code")
            self.show_frame("frame_series")
        except Exception as e:
            print(str(e))

class frame_series(frame):

    #gets e sets
    def get_selected_series(self):
        try:
            series_selecionadas=self.frame_objeto.get_selected_obj()
            return series_selecionadas
        except Exception as e:
            print(str(e))

    def get_series_by_type(self,**kwargs):
        try:
            series_selecionadas = []
            for instancia in instancias_processamento:
                [series_selecionadas.append(serie) for serie in instancia.filtrar_series(["normal","previsao","analize"])]
            return series_selecionadas
        except Exception as e:
            print(str(e))

    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_series",container)
        self.container=container
        self.frames_series=[]
        self.icones = load_icons(CAMINHO_ICONS_FRAME_SERIES, ".png")

    def load_series(self,series_temporais):
        try:
            self.frames_series=[]
            self.frame_objeto.clear_frame_widgets()
            for serie in series_temporais:
                self.frame_objeto.add_objeto(serie,serie.text_legenda,serie.is_select)
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.frame_objeto=frame_objetos_list(self,self.selecionar_serie,self.abrir_informacoes_serie,None,270,50,1)
            self.frame_objeto.pack(fill=tk.BOTH,expand=1)

            self.barra_opcoes=tk.Frame(self,height=30)
            self.barra_opcoes.pack(side=tk.TOP,fill=tk.X)

            self.botao_add=tk.Button(self.barra_opcoes,command=self.abrir_frame_code)
            self.botao_add.config(image=self.icones["create_obj"],relief=tk.FLAT)
            self.botao_add.image=self.icones["create_obj"]
            self.botao_add.pack(side=tk.LEFT)

            self.botao_open = tk.Button(self.barra_opcoes,command=self.abrir_series)
            self.botao_open.config(image=self.icones["open"],relief=tk.FLAT)
            self.botao_open.image = self.icones["open"]
            self.botao_open.pack(side=tk.LEFT)

            self.botao_save = tk.Button(self.barra_opcoes,command=self.salvar_series_selecionadas)
            self.botao_save.config(image=self.icones["save"], relief=tk.FLAT)
            self.botao_save.image = self.icones["save"]
            self.botao_save.pack(side=tk.LEFT)

            series_selecionadas=self.get_series_by_type()
            self.load_series(series_selecionadas)

        except Exception as e:
            print(str(e))

    def selecionar_serie(self,serie):
        try:
            if(serie.is_ploted):
                serie.processamento.processamento_plot.selecionar_serie(serie,resetar_series_selecionadas=False,update_screen=True)
        except Exception as e:
            print(str(e))

    def abrir_informacoes_serie(self,serie):
        try:
            self.container.frame_info_serie.load_serie(serie)
            self.container.show_frame("frame_info_serie")
        except Exception as e:
            print(str(e))

    def abrir_frame_code(self):
        try:
            self.container.show_frame("frame_code")
        except Exception as e:
            print(str(e))

    def salvar_series_selecionadas(self):
        try:
            caminho_series_selecionadas=opendirectory()
            series_selecionadas=self.frame_objeto.get_selected_obj()
            for serie in series_selecionadas:
                serie.save(nome_arquivo=serie.get_name(),caminho_arquivo=caminho_series_selecionadas)
        except Exception as e:
            print(str(e))

    def abrir_series(self):
        try:
            filetypes=(("Series(.serie)", "*.serie;*.csv"), ("Serie temporais(.st)", "*.st*"))
            series_selecionadas=openfiles(filetypes=filetypes)
            print()
            if(series_selecionadas!="" or series_selecionadas!=None):
                for url_arq_serie in series_selecionadas:
                    processamento.instancia_selecionada._load_serie_temporal(url_arq_serie)
            self.frame_objeto.clear_objtos()
            self.load_series(self.get_series_by_type())
        except Exception as e:
            print(str(e))

    def key_press(self,event):
        print(event.key_char)


class frame_info_serie(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_info_serie",container)
        self.janela=janela
        self.container=container

    def func_teste2(self):
        histograma=self.serie_selecionada.histograma(20)
        data_rows=[]
        data_rows.append([key for key in histograma[0].keys()])
        for hist in histograma:
            data_rows.append([value for value in hist.values()])
        janela=janela_tabela(None,self.janela.top_level)
        janela.iniciar_componentes()
        janela.frame_janela_tabela.tabela.criar_tabela("teste")
        janela.frame_janela_tabela.set_tabela_data(0,data_rows)
        janela.frame_janela_tabela.iniciar_componentes()

    def load_serie(self,serie_temporal):
        try:
            informacoes={}
            informacoes["Quantidade dados"] = str(len(serie_temporal.ploted_data_y))
            informacoes["Legenda"]=serie_temporal.text_legenda
            informacoes["Data inicial"]=str(serie_temporal.date_inicial)
            informacoes["Data final"]=str(serie_temporal.date_final)

            self.serie_selecionada=serie_temporal
            self.frame_informacoes.clear_frames()
            self.frame_informacoes.informacoes=informacoes
            self.frame_informacoes.create_frames()
            self.focus_force()

            self.botao_teste=tk.Button(self,text="click",command=self.func_teste2)
            self.botao_teste.pack()

            self.bind("<Key>",self.key_event)

        except Exception as e:
            print(str())

    def func_teste(self):
        array=["(",self.serie_selecionada,"/",2.0,")","-",5.0]
        teste=processamento.instancia_selecionada.run_code(array)
        print(teste)

    def iniciar_componentes(self):
        try:
            self.frame_informacoes=frame_informacoes(self,2,{})
            self.frame_informacoes.place(relx=0,rely=0,relwidth=1,relheight=0.75)

            self.botao_plotar_serie=tk.Button(self,text="Plotar serie",command=self.func_plotar_serie)
            self.botao_estatisticas_serie=tk.Button(self,text="Estatísticas da Série",command=self.func_estatisticas_serie)
            self.botao_tabela_frequencia=tk.Button(self,text="Tabela frequência",command=self.func_janela_frequencia)

            self.botao_plotar_serie.place(relx=0.05,rely=0.75,relwidth=0.4,relheight=0.25)
            self.botao_estatisticas_serie.place(relx=0.55, rely=0.75, relwidth=0.4, relheight=0.25)

        except Exception as e:
            print(str(e))

    def func_plotar_serie(self):
        try:
            processamento.instancia_selecionada.processamento_plot.plot_serie(self.serie_selecionada,label=self.serie_selecionada.text_legenda)
        except Exception as e:
            print(str(e))

    def func_estatisticas_serie(self):
        try:
            criar_estatistica(self.serie_selecionada)

            frame_estatisticas=self.janela.get_frame_notebook("Estatísticas")
            frame_estatisticas.load_estatistica(-1)

            self.janela.show_notebook_frame("Estatísticas")
            self.janela.notebook.select(frame_estatisticas)
        except Exception as e:
            print(str(e))

    def func_janela_frequencia(self):
        pass

    def func_ir_tela_series(self):
        try:
            self.container.show_frame("frame_series")
        except Exception as e:
            print(str(e))

    def key_event(self,event):
        try:
            if(event.keycode==8):
                self.func_ir_tela_series()
        except Exception as e:
            print(str(e))

    def mouse_event_enter(self,event):
        try:
            self.focus_force()
        except Exception as e:
            print(str(e))

class frame_code(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_code",container)
        self.icones = load_icons(CAMINHO_ICONS_FRAME_CODE, ".png")

    def iniciar_componentes(self):
        try:
            self.div_botoes=tk.Frame(self)
            self.div_botoes.pack(fill=tk.X)
            self.div_botoes.config(background="gainsboro")
            self.set_config_obj(self.div_botoes,"background","whitesmoke")

            self.botao_run=tk.Button(self.div_botoes,text="RODAR",image=self.icones["run_code"],command=self.run_code)
            self.botao_run.image=self.icones["run_code"]
            self.botao_run.pack(side=tk.LEFT)

            self.frame_codigo=frame_code_text(self)
            self.frame_codigo.pack_propagate(False)
            self.frame_codigo.config(height=210)
            self.frame_codigo.iniciar_componentes()
            self.frame_codigo.pack(fill=tk.X)

            self.frame_code_result=frame_code_result(self)
            self.frame_code_result.pack_propagate(False)
            self.frame_code_result.config(height=75)
            self.frame_code_result.iniciar_componentes()
            self.frame_code_result.pack(fill=tk.X)
        except Exception as e:
            print(str(e))

    def run_code(self):
        try:
            resultado=decode_code(self.frame_codigo.get_codigo())
            if(isinstance(resultado,list)):
                self.frame_code_result.add_text_logs(str(resultado))
            elif(isinstance(resultado,int) or isinstance(resultado,str)):
                self.frame_code_result.add_text_logs("Ocorreu um erro ao ler:"+str(resultado))
        except Exception as e:
            print(str(e))
