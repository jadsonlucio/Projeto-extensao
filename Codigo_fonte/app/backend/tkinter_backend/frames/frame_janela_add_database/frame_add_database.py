import tkinter as tk
import os
from ...engine import ttk



from ...frames.frame import frame
from ...box import show_warning,openfile
from ...objetos import date_choice
from .....processamento import arquivo as file
from .....processamento.threading import criar_thread
from .....constantes import CAMINHO_DATABASE
from .....constantes import CAMINHO_METRICAS_DATABASE
from .....constantes import CAMINHO_SELECTED_DATABASE


class frame_add_database(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_add_database",container)
        self.iniciar_componentes()

    def iniciar_componentes(self):
        self.pack(fill="both",expand=1)

        self.label_select_database=ttk.Label(self,text="Selecione a planilha com os dados")
        self.label_select_database.pack(anchor=tk.W)

        self.frame_select_planilha=tk.Frame(self)
        self.frame_select_planilha.pack(anchor=tk.NW,fill=tk.X)

        self.button_search=ttk.Button(self.frame_select_planilha,text="Buscar",command=self.search_dataset)
        self.button_search.pack(side=tk.LEFT)

        self.label_path_database = ttk.Entry(self.frame_select_planilha)
        self.label_path_database.pack(side=tk.LEFT,fill=tk.X,expand=1)
        self.label_path_database.config(state="disable")

        self.frame_divisor=tk.Frame(self,height=20)
        self.frame_divisor.pack(anchor=tk.NW,fill=tk.X)

        self.label_select_initial_data=ttk.Label(self,text="selecione a data inicial das observações")
        self.label_select_initial_data.pack(anchor=tk.NW)

        self.data_inicial=date_choice(self)
        self.data_inicial.iniciar_componentes(2010, 2020)
        self.data_inicial.pack(anchor=tk.NW)

        self.frame_divisor2=tk.Frame(self,height=20)
        self.frame_divisor2.pack(anchor=tk.NW,fill=tk.X)

        self.label_select_period=ttk.Label(self,text="Selecione o periodo entre cada observação")
        self.label_select_period.pack(anchor=tk.NW)

        self.frame_select_period=tk.Frame(self)
        self.frame_select_period.pack(anchor=tk.NW,fill=tk.X)

        self.entry_time_steps=tk.Entry(self.frame_select_period,width=13)
        self.entry_time_steps.pack(side=tk.LEFT)

        self.periodo_box = ttk.Combobox(self.frame_select_period)
        self.periodo_box.config(justify=tk.CENTER, width=13)
        self.periodo_box['value'] = ["minuto(s)","hora(s)","dia(s)"]
        self.periodo_box['state'] = 'readonly'
        self.periodo_box.current(newindex=0)
        self.periodo_box.pack(side=tk.LEFT)

        self.frame_divisor3 = tk.Frame(self, height=20)
        self.frame_divisor3.pack(anchor=tk.NW, fill=tk.X)

        self.label_select_keys=ttk.Label(self,text="Adicione aqui os nomes dos atributos da planilha(seperados por virgula)")
        self.label_select_keys.pack(anchor=tk.NW)

        self.text_atributos=tk.Text(self,width=50, height=7)
        self.text_atributos.pack(anchor=tk.NW)

        self.button_confirm=ttk.Button(self,text="Confirmar",command=self.confirm)
        self.button_confirm.pack(anchor=tk.SE)

    def search_dataset(self):
        path_selected_file=openfile(parent=self.janela,title="selecione a planilha",
                                filetypes=(("Planilhas (xlsx)", "*.xlsx"), ("All files", "*.*")))
        self.label_path_database.config(state="enable")
        self.label_path_database.delete(0,tk.END)
        self.label_path_database.insert(0,path_selected_file)
        self.label_path_database.config(state="disable")

    def save_selected_database(self):
        database_file=file.abrir_arquivo(CAMINHO_SELECTED_DATABASE)
        file.salvar_array_arquivo(database_file,[self.dict_form["nome_tabela"]])

    def confirm(self):
        try:
            self.dict_form={
                "nome_tabela":None,
                "orientacao":"vertical",
                "periodo":self.periodo_box.get().replace("(s)",""),
                "time_steps":None,
                "data_inicial":self.data_inicial.get_data().strftime("%d/%m/%Y"),
                "keys_array":self.text_atributos.get("1.0",tk.END).replace("\n","")
            }
            path=self.label_path_database.get()
            time_steps=self.entry_time_steps.get()

            if(len(path)>0):
                self.dict_form["nome_tabela"]=os.path.basename(path)
            else:
                raise Exception("Nenhuma planilha selecionada")
            if(len(time_steps)):
                try:
                    self.dict_form["time_steps"]=int(time_steps)
                except:
                    raise Exception("Por favor digite somente numeros no campo periodo")
            else:
                raise Exception("Por favor preencha o campo periodo")

            file.copiar_arquivo(path, CAMINHO_DATABASE)
            array_form=file.converter_dictonary_to_array(self.dict_form)
            arquivo=file.criar_arquivo(self.dict_form["nome_tabela"]+".txt",CAMINHO_METRICAS_DATABASE)
            file.salvar_array_arquivo(arquivo,array_form)

            self.save_selected_database()

            if(self.janela.frame_inicial!=None):
                self.janela.frame_inicial.frame_erro.destroy()

                frame_inicial=self.janela.frame_inicial
                criar_thread(frame_inicial.carregar_database)
            if(self.janela.frame_database!=None):
                self.janela.frame_database.update_all_objects()
                self.janela.top_level.grab_set()

            self.janela.destroy()

        except Exception as e:
            show_warning("Erro",str(e))

