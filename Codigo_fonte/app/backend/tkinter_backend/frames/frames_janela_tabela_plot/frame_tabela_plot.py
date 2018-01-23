import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame



class frame_tabela_plot(tk.LabelFrame):

    def clear_widget(self,widget):
        for child in widget.winfo_children():
            child.destroy()

    def __init__(self, janela, container,frame_tabela):
        tk.LabelFrame.__init__(self, container,text="Opções de plot")
        self.janela=janela
        self.frame_tabela=frame_tabela


    def iniciar_componentes(self):
        try:
            self.text_tipo_plot = tk.Label(self, text="Tipo de gráfico")
            self.text_tipo_plot.pack(anchor=tk.NW)
            self.box_tipo_plot=ttk.Combobox(self)
            self.box_tipo_plot["value"]=["Gráfico de linhas","Gráfico de barras","Correreogramo","Boxplot","Histograma"]
            self.box_tipo_plot["state"]="readonly"
            self.box_tipo_plot.current(newindex=0)
            self.box_tipo_plot.pack(anchor=tk.NW)
            self.box_tipo_plot.bind("<<ComboboxSelected>>", self.func_selecionar_tipo_plot)

            self.frame_opcoes_plot=tk.Frame(self)
            self.frame_opcoes_plot.pack(fill=tk.BOTH,expand=1,anchor=tk.NW)

        except Exception as e:
            print(str(e))

    def func_selecionar_tipo_plot(self,event):
        try:
            self.frame_opcoes_plot.destroy()
            tipo_plot=self.box_tipo_plot.get()
            if(tipo_plot=="Gráfico de linhas"):
                self.frame_opcoes_plot = tk.Frame(self)
                self.frame_opcoes_plot.config(background="snow")
                self.frame_opcoes_plot.pack(fill=tk.BOTH,expand=1,anchor=tk.NW)

                dados_coluna=self.frame_tabela.tabela.get_row_planilha(index_planilha=0,index_row=0,min_col=0,max_col=None)

                self.text_select_col=tk.Label(self.frame_opcoes_plot,text="Selecione a coluna de dados")
                self.text_select_col.pack(anchor=tk.W)
                self.box_dados_plot=ttk.Combobox(self.frame_opcoes_plot)
                self.box_dados_plot["value"]=dados_coluna
                self.box_dados_plot['state'] = 'readonly'
                self.box_dados_plot.current(newindex=0)
                self.box_dados_plot.pack(anchor=tk.W)


        except Exception as e:
            print(str(e))