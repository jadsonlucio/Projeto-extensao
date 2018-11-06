import tkinter as tk
from time import sleep
from tkinter import ttk, Frame

from app.processamento.exceptions.exception import infoerroexception,tratamento_excessao
from app.processamento.datas import month_range,date
from app.processamento.threading import thread

class load_frame(Frame):
    def __init__(self, container, mode='indeterminado', text_var=None, bar_var=None, bar_maxvalue=0, **kwargs):
        Frame.__init__(self, container)
        self.container=container
        self.ativacao = True
        self.text_var = text_var
        self.bar_var = bar_var
        self.bar_maxvalue = bar_maxvalue
        self.ativacao = False
        self.mode = mode

    #funcao de criação

    def show_load(self):
        try:
            self.ativacao = True
            self.text_bar = tk.Label(self, textvariable=self.text_var)
            self.text_bar.pack(anchor=tk.CENTER, side=tk.BOTTOM)
            if (self.mode == 'daterminado'):
                self.load_bar = ttk.Progressbar(self, variable=self.bar_var, maximum=self.bar_maxvalue)
                self.load_bar.pack(anchor=tk.CENTER, side=tk.BOTTOM, fill=tk.X)
            elif (self.mode == 'indeterminado'):
                self.thread = thread(self.update_thread)
                self.thread.start()
        except Exception as e:
            tratamento_excessao(type_exception='Erro')

    #função loop load

    def update_thread(self):
        try:
            if (self.mode == 'indeterminado'):
                array_carregando = ['Carregando.  ', ' Carregando.. ', 'Carregando...']
                while (self.ativacao):
                    for array in array_carregando:
                        self.text_var.set(array)
                        sleep(0.2)
        except Exception as e:
            tratamento_excessao(type_exception='Info')

    #função finalizar load

    def hide_load(self):
        self.ativacao = False
        self.destroy()


class aba(Frame):

    #geters e seters

    def set_estado(self, state='ativado'):
        if (state == 'ativado'):
            self.botao.config(background=self.select_color)
            self.botao_fechar.config(background=self.select_color)
            self.is_select = True
        if (state == 'desativado'):
            self.botao.config(background=self.notselect_color)
            self.botao_fechar.config(background=self.notselect_color)
            self.is_select = False

    def set_funcbotao(self, func):
        self.botao.bind('<Button-1>', lambda event: func(self))

    def set_funcbotao_fechar(self, func):
        self.botao_fechar.bind('<Button-1>', lambda event: func(self))


    def __init__(self, container):
        Frame.__init__(self, container)
        self.frame_aba = container
        self.select_color = 'Gainsboro'
        self.notselect_color = 'white'
        self.is_select = False

    #função de criação

    def criar_aba(self, text_var, text_size):
        self.text_var = text_var
        self.text_size = text_size
        self.botao = tk.Button(self, textvariable=text_var, width=text_size)
        self.botao.config(relief='flat')
        self.botao.pack(side=tk.LEFT)
        self.botao_fechar = tk.Button(self, text='x')
        self.botao_fechar.config(relief='flat')
        self.botao_fechar.pack(side=tk.LEFT)
        self.config(highlightbackground="gray", highlightcolor="gray", highlightthickness=1)


    #funções classe

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
    def set_current_instancia(cls, instancia):
        cls.current_instancia = instancia


class aba_frame(Frame):
    instancias = []
    instancia_selecionada = None

    def __init__(self, container, func_ativacao=None,func_exclusao=None):
        Frame.__init__(self, container)
        self.abas = []
        self.current_aba = None
        self.func_ativacao = func_ativacao
        self.func_exclusao=func_exclusao
        aba_frame.instancia_selecionada = self

    #função criação

    def add_aba(self, dict, arg):
        frame_aba = aba(self)
        frame_aba.criar_aba(tk.StringVar(), 10)
        frame_aba.text_var.set('Nova aba')
        frame_aba.pack(side=tk.LEFT)
        frame_aba.set_funcbotao(self.selecionar_aba)
        frame_aba.set_funcbotao_fechar(self.excluir_aba)

        dict[frame_aba] = arg

        self.dict = dict
        self.abas.append(frame_aba)
        self.selecionar_aba(frame_aba)

    #funções abas

    def excluir_aba(self, aba):
        if (len(self.abas) > 1):

            for cont in range(len(self.abas)):
                if (self.abas[cont] == aba and aba == self.current_aba):
                    self.current_aba = None
                    if (cont == len(self.abas) - 1):
                        self.selecionar_aba(self.abas[-2])
                    else:
                        self.selecionar_aba(self.abas[cont + 1])
            self.func_exclusao(aba)
            self.dict[aba].destroy()
            self.abas.remove(aba)
            aba.destroy()

    def selecionar_aba(self, aba):
        if (self.current_aba):
            self.current_aba.set_estado('desativado')
        self.current_aba = aba
        self.current_aba.set_estado('ativado')
        self.func_ativacao(self.current_aba)


class date_choice(Frame):
    def __init__(self, container):
        Frame.__init__(self, container)
        self.container = container

    #função de criação

    def iniciar_componentes(self, ano_inicial, ano_final):
        try:
            self.dia_text = tk.Label(self, text='dia')
            self.dia_box = ttk.Combobox(self)
            self.dia_box.config(justify=tk.CENTER, width=2, height=5, state='readonly')
            self.mes_text = tk.Label(self, text='mês')
            self.mes_box = ttk.Combobox(self)
            self.mes_box.config(justify=tk.CENTER, width=2, height=5, state='readonly')
            self.ano_text = tk.Label(self, text='ano')
            self.ano_box = ttk.Combobox(self)
            self.ano_box.config(justify=tk.CENTER, width=4, height=5, state='readonly')
            self.dia_box.grid(row=1, column=0)
            self.dia_text.grid(row=0, column=0)
            self.mes_box.grid(row=1, column=1)
            self.mes_text.grid(row=0, column=1)
            self.ano_box.grid(row=1, column=2)
            self.ano_text.grid(row=0, column=2)
            self.dias = [cont for cont in range(1, month_range(1, ano_inicial)[1] + 1)]
            self.meses = [cont for cont in range(1, 13)]
            self.anos = [cont for cont in range(ano_inicial, ano_final + 1)]
            self.dia_box['value'] = self.dias
            self.mes_box['value'] = self.meses
            self.ano_box['value'] = self.anos
            self.dia_box.current(0)
            self.mes_box.current(0)
            self.ano_box.current(0)
            self.mes_box.bind('<<ComboboxSelected>>', lambda event: self.atualizar_data())
            self.ano_box.bind('<<ComboboxSelected>>', lambda event: self.atualizar_data())
            self.dia_text.config(background='gainsboro')
            self.mes_text.config(background='gainsboro')
            self.ano_text.config(background='gainsboro')
            self.config(background='gainsboro')

        except Exception as e:
            tratamento_excessao('Erro')

    #funções de datas

    def atualizar_data(self):
        try:
            dia = int(self.dia_box.get())
            mes = int(self.mes_box.get())
            ano = int(self.ano_box.get())
            self.dias = [cont for cont in range(1, month_range(mes, ano)[1] + 1)]
            if (self.dias[-1] < dia):
                current = 0
            else:
                current = dia - 1
            self.dia_box['value'] = self.dias
            self.dia_box.current(current)
        except Exception as e:
            tratamento_excessao('Erro')

    def get_data(self):
        try:
            dia = int(self.dia_box.get())
            mes = int(self.mes_box.get())
            ano = int(self.ano_box.get())
            return date(day=dia, month=mes, year=ano)
        except Exception as e:
            tratamento_excessao('Erro')

class frame_scroll(tk.Frame):

    def set_scrollregion(self,array=None):
        try:
            if(array==None):
                array=[valor for valor in self.canvas.bbox("all")]
                array[3]=array[3]+20
                array[2]=array[2]+20
                self.canvas.config(scrollregion=tuple(array))
            else:
                self.canvas.config(scrollregion=([valor for valor in array]))
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,container,scroll_size=16):
        Frame.__init__(self,container)
        self.container=container
        self.scroll_size=scroll_size

    def iniciar_componentes(self):
        self.canvas=tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
        self.scrollbary = ttk.Scrollbar(self, command=self.canvas.yview)
        self.scrollbarx = ttk.Scrollbar(self, command=self.canvas.xview,orient=tk.HORIZONTAL)

        self.canvas.configure(yscrollcommand=self.scrollbary.set,xscrollcommand=self.scrollbarx.set)

        self.frame_widgets=tk.Frame(self.canvas)
        self.frame_canvas=self.canvas.create_window((0, 0), window=self.frame_widgets, anchor='nw')

        self.canvas.bind('<Configure>', self.event_canvas_configure)
        self.bind('<Configure>',self.frame_event_configure)

    def event_canvas_configure(self,event):
        self.set_scrollregion()

    def frame_event_configure(self,event):
        self.scrollbary.place(x=event.width-self.scroll_size,y=0,width=self.scroll_size,relheight=1.0)
        self.scrollbarx.place(x=0, y=event.height - self.scroll_size, relwidth=1.0, height=self.scroll_size)

    def clear_frame_widgets(self):
        try:
            for obj in self.frame_widgets.winfo_children():
                if(isinstance(obj,tk.Widget)):
                    obj.destroy()
        except Exception as e:
            tratamento_excessao("Erro")

class frame_objetos_list(frame_scroll):
    def __init__(self,container,func_right_click,func_left_click,objetos,width_objeto,height_objeto,max_columns):
        frame_scroll.__init__(self,container)
        self.iniciar_componentes()
        self.container=container
        self.frames_objeto={}
        self.func_right_click=func_right_click
        self.func_left_click=func_left_click
        self.width_objeto=width_objeto
        self.height_objeto=height_objeto
        self.max_columns=max_columns
        if(objetos==None):
            self.objetos=[]
        else:
            self.objetos=objetos
        self.current_col=0
        self.current_row=0

    def add_objeto(self,objeto,text_objeto,select,func_right_click=None,func_left_click=None,width_objeto=None,height_objeto=None,column=None,row=None):
        try:
            frame_obj=frame_objeto(self.frame_widgets,objeto,self.func_right_click,self.func_left_click,text_objeto,select,self.width_objeto,
                                          self.height_objeto,self.current_col,self.current_row)

            frame_obj.iniciar_componente()

            self.current_col=self.current_col+1
            if(self.current_col==self.max_columns):
                self.current_col=0
                self.current_row=self.current_row+1

            self.objetos.append(objeto)
            self.frames_objeto[objeto]=frame_obj
            self.set_scrollregion()
        except Exception as e:
            tratamento_excessao("Erro")


    def remove_objeto(self,objeto):
        try:
            self.frames_objeto[objeto].destroy()
            self.objetos.remove(objeto)
        except Exception as e:
            tratamento_excessao("Erro")

    def clear_objtos(self):
        try:
            for objeto in self.objetos:
                self.remove_objeto(objeto)
        except Exception as e:
            tratamento_excessao("Erro")

    def get_selected_obj(self):
        try:
            array_objetos=[]
            for objeto in self.objetos:
                frame_objeto=self.frames_objeto[objeto]
                if(frame_objeto.select):
                    array_objetos.append(objeto)
            return array_objetos
        except Exception as e:
            tratamento_excessao("Erro")


class frame_objeto(Frame):
    def __init__(self,container,objeto,func_right_click,func_left_click,text_objeto,select,width_objeto,height_objeto,column_grid,row_grid):
        Frame.__init__(self,container)
        self.container=container
        self.func_left_click=func_left_click
        self.func_right_click=func_right_click
        self.objeto=objeto
        self.text_objeto=text_objeto
        self.select=select
        self.width_objeto=width_objeto
        self.height_objeto=height_objeto
        self.column=column_grid
        self.row=row_grid

    def iniciar_componente(self):
        try:
            self.text_label=tk.Label(self,text=self.text_objeto,font=("Arial",int(self.height_objeto/4)))
            self.text_label.pack(side=tk.LEFT)

            self.config(width=self.width_objeto,height=self.height_objeto
                        ,borderwidth=3,relief=tk.GROOVE)
            self.pack_propagate(False)
            self.grid(row=self.row,column=self.column)
            self.bind("<Button-1>",self.funcao_left_click)
            self.text_label.bind("<Button-1>",self.funcao_left_click)
            self.bind("<Button-3>", self.funcao_right_click)
            self.text_label.bind("<Button-3>", self.funcao_right_click)
            self.funcao_selecao()
        except Exception as e:
            tratamento_excessao("Erro")

    def funcao_left_click(self,event):
        try:
            if(self.func_left_click!=None):
                self.func_left_click(self.objeto)
        except Exception as e:
            tratamento_excessao("Erro")

    def funcao_right_click(self,event):
        try:
            self.select=not self.select
            self.funcao_selecao()
            if(self.func_right_click!=None):
                self.func_right_click(self.objeto)
        except Exception as e:
            tratamento_excessao("Erro")

    def funcao_selecao(self,select=None):
        try:
            if(select!=None):
                self.select=select
            if(self.select):
                self.text_label.config(background="dodgerblue")
                self.config(background="dodgerblue")
            else:
                self.text_label.config(background="gainsboro")
                self.config(background="gainsboro")
        except Exception as e:
            tratamento_excessao("Erro")

class frame_informacoes(Frame):

    def set_informacoes(self,dirt_informacoes):
        try:
            self.informacoes=dirt_informacoes
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,container,max_col,dirt_informacoes=None):
        Frame.__init__(self,container)
        self.container=container
        self.informacoes=dirt_informacoes
        self.frames_info={}
        self.max_col=max_col
        self.current_row=0
        self.current_col=0

    def clear_frames(self):
        try:
            for child in self.winfo_children():
                child.destroy()
            self.frames_info.clear()
            self.current_row=0
            self.current_col=0
        except Exception as e:
            tratamento_excessao("Erro")

    def create_frames(self):
        try:
            tamanho_y=1/((len(self.informacoes)-(len(self.informacoes)%self.max_col))/self.max_col+1)
            tamanho_x=1/self.max_col

            for key,value in zip(self.informacoes.keys(),self.informacoes.values()):
                frame=tk.Frame(self)
                frame.place(relx=self.current_col*tamanho_x, rely=self.current_row*tamanho_y, relheight=tamanho_y, relwidth=tamanho_x)
                frame.config(background="ghostwhite",relief=tk.RIDGE,borderwidth=1)
                frame.bind("<Enter>",self.func_enter_frame)
                frame.bind("<Leave>",self.func_leave_frame)

                text_key=tk.Label(frame,text=key)
                text_value=tk.Label(frame,text=value)
                text_key.pack(anchor=tk.NW)
                text_value.pack(anchor=tk.CENTER,fill=tk.Y,expand=1)
                self.current_col=self.current_col+1
                if(self.current_col==self.max_col):
                    self.current_col=0
                    self.current_row=self.current_row+1
                self.frames_info[key]=frame
        except Exception as e:
            tratamento_excessao("Erro")

    def func_enter_frame(self,event):
        try:
            widget=event.widget
            for child in widget.winfo_children():
                child.config(background="lightgray")
            widget.config(background="lightgray")
        except Exception as e:
            tratamento_excessao("Erro")

    def func_leave_frame(self,event):
        try:
            widget=event.widget
            for child in widget.winfo_children():
                child.config(background="ghostwhite")
            widget.config(background="ghostwhite")
        except Exception as e:
            tratamento_excessao("Erro")


#frame code objects

class frame_code_text(Frame):
    #gets e sets

    def get_codigo(self,linha=None):
        try:
            codigo=self.text.get("1.0",tk.END)
            return codigo
        except Exception as e:
            tratamento_excessao("Erro")

    def set_code(self,text):
        try:
            self.text.delete(1.0, tk.END)
            self.text.insert(1.0, text)
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,container):
        Frame.__init__(self,container)

    def iniciar_componentes(self):
        try:
            self.scroll_y = ttk.Scrollbar(self)
            self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

            self.text = tk.Text(self)
            self.text.config(yscrollcommand=self.scroll_y.set)
            self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scroll_y.config(command=self.text.yview)
        except Exception as e:
            tratamento_excessao("Erro")


class frame_code_result(Frame):
    def __init__(self,container):
        Frame.__init__(self,container)

    def add_text_logs(self,text):
        try:
            self.text.configure(state='normal')
            self.text.insert('end',">"+text+"\n")
            self.text.configure(state='disabled')
        except Exception as e:
            tratamento_excessao("Erro")

    def iniciar_componentes(self):
        try:
            self.scroll_y = ttk.Scrollbar(self)
            self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

            self.text = tk.Text(self)
            self.text.config(yscrollcommand=self.scroll_y.set)
            self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scroll_y.config(command=self.text.yview)
        except Exception as e:
            tratamento_excessao("Erro")