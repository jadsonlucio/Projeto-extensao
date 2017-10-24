from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import style

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels.api as sm

from .....constantes import STYLE_PYPLOT,SUBPLOT_SELECT_COLOR,SUBPLOT_NOT_SELECT_COLOR

import tkinter as tk
from ...engine import ttk
from ..frame import frame
from ...objetos import aba_frame

from .....instancias.Instancias import add_instancia,get_instancia
from .....processamento.series_temporais.processamento import processamento

style.use(STYLE_PYPLOT)

class frame_grafico(frame):
    def __init__(self, janela, container):
        frame.__init__(self, janela, 'frame_grafico', container)
        self.frames = {}
        self.janela = janela
        self.iniciar_componentes()

    #funcões abas

    def criar_grafico(self):
        try:
            if (len(aba_frame.instancia_selecionada.abas) < 10):
                frame_graph = frame_plot(self.janela, self.frame_grafico, None)
                frame_graph.criar_figura(len(self.frame_abas.abas))

                self.frame_abas.add_aba(self.frames, frame_graph)
                self.frames[self.frame_abas.current_aba] = frame_graph

                frame_graph.botao_aba = self.frame_abas.current_aba
        except Exception as e:
            print(str(e))

    def selecionar_grafico(self, frame_aba):
        try:
            frame_graph = self.frames[frame_aba]
            frame_plot.instancia_selecionada = frame_graph
            frame_graph.raise_frame()
            processamento.set_instancia_selecionada(frame_graph.processamento)
        except Exception as e:
            print(str(e))

    def mudar_tempo_grafico(self,periodo,time_steps,text_time):
        frame_plot_selecionado=frame_plot.get_current_instacia()
        series_selecionadas=frame_plot_selecionado.processamento.get_series_selecionadas()
        processamento_plot=frame_plot_selecionado.processamento.processamento_plot
        for serie in series_selecionadas:
            serie.mudar_tempo_serie(periodo, time_steps)
            if (serie.text_legenda != None):
                processamento_plot.plot_serie(serie,label=serie.text_legenda + ',' + text_time,selecionar_serie=False,
                                                                      update_screen=False,index_subplot=serie.subplot)
                processamento_plot.selecionar_serie(serie,resetar_series_selecionadas=False,update_screen=False)
            else:
                processamento_plot.plot_serie(serie,selecionar_serie=False,update_screen=False,index_subplot=serie.subplot)
                processamento_plot.selecionar_serie(serie,resetar_series_selecionadas=False,update_screen=False)
        frame_plot_selecionado.update_screen()

    #funcões de criação

    def iniciar_componentes(self):
        try:
            self.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

            self.div1 = tk.Frame(self, height=30)
            self.div1.pack_propagate(False)
            self.div1.pack(fill=tk.X)

            self.text_times=['MN','S1','D1','H4','H1','M10']
            self.periodos_time_steps=[['dia',30],['dia',7],['dia',1],['hora',4],['hora',1],['minuto',10]]

            self.button_time_change=[]
            for text,array in zip(self.text_times,self.periodos_time_steps):
                botao=tk.Button(self.div1,text=text,command=lambda periodo=array[0],time_steps=array[1],text_time=text :self.mudar_tempo_grafico(periodo,time_steps,text_time))
                botao.pack(side=tk.RIGHT)

            self.frame_abas = aba_frame(self, self.selecionar_grafico)
            self.frame_abas.pack(anchor=tk.W)

            self.botao_add_aba = tk.Button(self.frame_abas, text="+", command=self.criar_grafico)
            self.botao_add_aba.pack(side=tk.RIGHT)

            self.frame_grafico = tk.Frame(self, background='blue')
            self.frame_grafico.pack(fill=tk.BOTH, expand=1)
            self.frame_grafico.grid_columnconfigure(0, weight=1)
            self.frame_grafico.grid_rowconfigure(0, weight=1)

            self.criar_grafico()
        except Exception as e:
            print(str(e))


class frame_plot(frame):
    instancias = []
    instancia_selecionada = None

    # funcões de geters e sets

    def get_lines_axes(self, index):
        if(isinstance(index,int)):
            subplot=self.subplots[0]
        else:
            subplot=index
        return subplot.lines

    def get_lines_lengenda(self, index):
        if(isinstance(index,int)):
            subplot = self.subplots[index]
        else:
            subplot=index

        return subplot.legend().get_lines()

    def get_visible_lines(self,index):
        try:
            array_linhas_visiveis=[]
            if (isinstance(index, int)):
                subplot = self.subplots[0]
            else:
                subplot = index
            for linha in subplot.lines:
                if(linha.get_visible()):
                    array_linhas_visiveis.append(linha)
            return array_linhas_visiveis
        except Exception as e:
            print(str(e))

    def get_serie_line2d(self,line2d):
        try:
            linha = []
            for subplot in self.figura.axes:
                for linha_legenda,linha_serie in zip(self.legendas[subplot].get_lines(),subplot.lines):
                    if(line2d==linha_legenda):
                        linha='linha legenda',self.processamento.get_time_serie(linha_serie)
                    if(line2d==linha_serie):
                        linha='linha grafico',self.processamento.get_time_serie(linha_serie)
            if(len(linha)>0):
                 return linha[1],linha[0]
            else:
                 raise ValueError("Não foi possivel encontra a serie selecionada")
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print(str(e))

    def get_subplot(self, index, copy=False):
        self.subplots = self.figura.axes
        if (copy == False):
            return self.figura.axes[index], len(self.subplots)
        else:
            return self.subplots[:][index], len(self.subplots)

    def get_subplot_line2d(self,line_2d):
        try:
            cont=0
            for subplot in self.figura.axes:
                for linha in subplot.lines:
                    if(linha==line_2d):
                        return subplot,cont
                cont=cont+1
        except Exception as e:
            print(str(e))

    def __init__(self, janela, container, botao_aba, **kwargs):
        frame.__init__(self, janela, 'frame_plot', container)
        frame_plot.add_instancia(self)
        self.kwargs = kwargs
        self.processamento = processamento(self)
        self.current_plot=""
        self.botao_aba = botao_aba

    #raise frame

    def raise_frame(self):
        try:
            self.tkraise()
            frame_plot.set_current_instancia(self)
        except Exception as e:
            print(str(e))

    #funcões de criacao

    def criar_figura(self, valor):
        try:
            self.figura = Figure(figsize=(5, 5), dpi=100)
            self.figura.subplots_adjust(bottom=0.09, top=0.95, left=0.05, right=0.96)
            self.canvas = FigureCanvasTkAgg(figure=self.figura, master=self)
            self.figura.canvas = self.canvas
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            toolbar = NavigationToolbar2TkAgg(self.canvas, self)
            toolbar.update()

            self.grid(row=0, column=0, sticky=tk.NSEW)
            self.pick_event=self.figura.canvas.mpl_connect('pick_event',self.on_pick)
            self.click_event=self.figura.canvas.mpl_connect('button_press_event',self.on_click)

        except Exception as e:
            print(str(e))

    #funcões subplot

    def add_subplot(self, column=1):
        self.size_subplots = len(self.figura.axes)
        self.figura.add_subplot(self.size_subplots + 1 , column, self.size_subplots + 1)
        self.subplots = self.figura.axes

    def excluir_subplot(self,index):
        if(isinstance(index,int)):
            self.figura.delaxes(self.subplots[index])
            self.size_subplots=len(self.figura.axes)
            self.subplots=self.figura.axes
            if(len(self.subplots)>0):
                self.selecionar_subplot(0)
        else:
            self.figura.delaxes(index)
            self.size_subplots = len(self.figura.axes)
            self.subplots = self.figura.axes
            if (len(self.subplots) > 0):
                self.selecionar_subplot(0)

    def verificar_subplots(self):
        if (len(self.figura.axes) == 0):
            self.legendas = {}
            self.add_subplot(1)
            self.selecionar_subplot(0)

    def selecionar_subplot(self, index):
        try:
            if(isinstance(index,int)):
                self.subplot_selecionado = self.subplots[index]
            else:
                self.subplot_selecionado=index
            for subplot in self.figura.axes:
                if(subplot==self.subplot_selecionado):
                    subplot.set_facecolor(SUBPLOT_SELECT_COLOR)
                else:
                    subplot.set_facecolor(SUBPLOT_NOT_SELECT_COLOR)
        except Exception as e:
            print(str(e))

    # funcões de atualização

    def update_legenda(self, *args, **kwargs):
        try:
            for subplot in self.figura.axes:
                handles,labels=subplot.get_legend_handles_labels()
                self.legendas[subplot]=subplot.legend(handles,labels)
                if(self.legendas[subplot]!=None):
                    for linha in self.legendas[subplot].get_lines():
                        linha.set_picker(5)
        except Exception as e:
            print(str(e))

    def update_escala(self,visible_only=True):
        try:
            for subplot in self.figura.axes:
                if(len(self.get_visible_lines(subplot))>0):
                    subplot.relim(visible_only=visible_only)
                    subplot.autoscale_view(True, True, True)
                else:
                    subplot.relim(visible_only=visible_only)
                    subplot.autoscale_view(False, False, False)
        except Exception as e:
            print(str(e))

    def update_subplots(self):
        for subplot in self.figura.axes:
            if(len(subplot.lines)==0 and self.current_plot=="Normal"):
                self.excluir_subplot(subplot)
        quant_subplots = len(self.figura.axes)
        cont_subplot = 1
        for subplot in self.figura.axes:
            subplot.change_geometry(quant_subplots, 1, cont_subplot)
            cont_subplot += 1

    def update_canvas(self, *args, **kwargs):
        self.canvas.show()

    def update_screen(self):
        try:
            self.update_subplots()
            self.update_escala(self.subplot_selecionado)
            self.update_legenda()
            self.update_canvas()
        except Exception as e:
            print(str(e))

    # funcões de plotagem

    def plot_normal(self, data_x, data_y, x_label, y_label, index_axes=-1, **kwargs):
        try:
            if(self.current_plot!="Normal"):
                self.figura.clear()
            self.verificar_subplots()
            if(isinstance(index_axes,int)):
                if(index_axes==-1):
                    subplot=self.subplot_selecionado
                elif(index_axes>=0):
                    subplot= self.figura.axes[index_axes]
            else:
                subplot=index_axes
            line_2d,=subplot.plot(data_x,data_y,**kwargs)
            self.subplot_selecionado.set_xlabel(x_label)
            self.subplot_selecionado.set_ylabel(y_label)
            self.current_plot="Normal"
            line_2d.set_picker(5)
            return line_2d,subplot
        except Exception as e:
            print(str(e))

    def box_plot(self,data,**kwargs):
        try:
            if(self.current_plot!="Boxplot"):
                self.figura.clear()
            self.verificar_subplots()
            self.subplot_selecionado.boxplot(data,**kwargs)
            self.current_plot="Boxplot"
        except Exception as e:
            print(str(e))

    def plot_bar(self,array_valores,array_text):
        pass

    def plot_scatter(self,data_x,data_y,**kwargs):
        if(self.current_plot!="Scatter"):
            self.figura.clear()
            self.verificar_subplots()
        self.subplot_selecionado.plot(data_x,data_y,'o',**kwargs)
        self.current_plot="Scatter"

    def plot_histograma(self,array_valores,quantidade_classes,normed=False,**kwargs):
        try:
            if (self.current_plot != "Histogram"):
                self.figura.clear()
                self.verificar_subplots()
            self.subplot_selecionado.hist(array_valores,quantidade_classes,normed=normed,**kwargs)
            self.update_canvas()
            self.current_plot="Histogram"
        except Exception as e:
            print(str(e))

    def plot_autocorrelacao(self,data_y,titulo="Autocorrelação",tipo_plot="pacf",lags=None,alpha=0.05,**kwargs):
        if(self.current_plot!="Autocorrelação"):
            self.figura.clear()
            self.verificar_subplots()
        if(tipo_plot=="pacf"):
            sm.graphics.tsa.plot_pacf(data_y,ax=self.subplot_selecionado,title=titulo,lags=lags,alpha=alpha,**kwargs)
        elif(tipo_plot=="acf"):
            sm.graphics.tsa.plot_acf(data_y, ax=self.subplot_selecionado,title=titulo,lags=lags,alpha=alpha,**kwargs)
        self.current_plot="Autocorrelação"

    #funcões eventos

    def on_motion(self,event):
        try:
            pass
        except Exception as e:
            print(str(e))

    def on_figure_enter(self,event):
        try:
            pass
        except Exception as e:
            print(str(e))

    def on_figure_leave(self,event):
        try:
            pass
        except Exception as e:
            print(str(e))

    def on_axes_enter(self,event):
        try:
            pass
        except Exception as e:
            print(str(e))

    def on_axes_leave(self,event):
        try:
            pass
        except Exception as e:
            print(str(e))

    def on_click(self,event):
        try:
            self.canvas.get_tk_widget().focus_force()
            subplot=event.inaxes
            if(subplot!=None and subplot!=self.subplot_selecionado and not self.click_pick_event):
                self.selecionar_subplot(subplot)
                self.update_canvas()
            self.click_pick_event = False
        except Exception as e:
            print(str(e))

    def on_pick(self,event):
        try:
            self.click_pick_event=True
            objeto=event.artist
            evento_mouse=event.mouseevent
            key=evento_mouse.key
            serie,tipo_linha=self.get_serie_line2d(objeto)
            if(tipo_linha=='linha grafico'):
                if(key==None):
                    self.processamento.processamento_plot.selecionar_serie(serie,True,True)
                elif(key=='alt'):
                    self.processamento.processamento_plot.selecionar_serie(serie,True,False)
            if(tipo_linha=='linha legenda'):
                if(evento_mouse.button==1):
                    self.processamento.processamento_plot.selecionar_serie(serie, True, True)
                if(evento_mouse.button==2):
                    self.processamento.processamento_plot.selecionar_serie(serie, True, True)
                if(evento_mouse.button==3):
                    dirt= self.janela.get_mouse_position()
                    self.criar_menu_opcoes(serie, dirt["x"], dirt["y"])

        except Exception as e:
            print(str(e))

    def on_key_press(self,event):
        try:
            print(event.key)
        except Exception as e:
            print(str(e))

    def on_key_release(self,event):
        try:
            pass
        except Exception as e:
            print(str(e))

    # função criacão menu opções

    def criar_menu_mover_plot(self,serie,menu_opcoes):
        try:
            def mover_novo_subplot():
                self.add_subplot(1)
                self.selecionar_subplot(-1)
                self.processamento.processamento_plot.move_plot_serie(serie,index_subplot=-1)

            menu_mover_plot=tk.Menu(menu_opcoes,tearoff=0)
            menu_opcoes.add_cascade(label="Mever para", menu=menu_mover_plot)

            cont=0
            for subplot in self.subplots:
                if(subplot!=serie.subplot):
                    menu_mover_plot.add_command(label="Subplot "+str(cont+1),command= lambda index_subplot=cont :
                         self.processamento.processamento_plot.move_plot_serie(serie,index_subplot=index_subplot))
                cont=cont+1

            menu_mover_plot.add_command(label="Novo subplot",command=lambda :mover_novo_subplot())
        except Exception as e:
            print(str(e))

    def criar_menu_opcoes(self,serie,mouse_x,mouse_y):
        try:
            menu_opcoes = tk.Menu(self, tearoff=0)
            menu_opcoes.add_command(label="Excluir",command=lambda :self.processamento.processamento_plot.excluir_plot_serie(serie,True))
            menu_opcoes.add_command(label="Esconder/Mostrar",command=lambda :self.processamento.processamento_plot.mudar_visibilidade_plot_serie(serie,True))
            self.criar_menu_mover_plot(serie,menu_opcoes)
            menu_opcoes.post(mouse_x,mouse_y)
        except Exception as e:
            print(str(e))

    # metodos classe
    @classmethod
    def add_instancia(cls, instancia):
        cls.instancias.append(instancia)

    @classmethod
    def remove_instancia(cls, instancia):
        cls.instancias.remove(instancia)

    @classmethod
    def get_instances(cls):
        return cls.instancias

    @classmethod
    def get_current_instacia(cls):
        return cls.instancia_selecionada

    @classmethod
    def set_current_instancia(cls, instancia):
        cls.current_instancia = instancia

def criar_frame_grafico(janela,container):
    inst_frame_grafico=frame_grafico(janela,container)
    add_instancia('frame_grafico',inst_frame_grafico)
    return inst_frame_grafico