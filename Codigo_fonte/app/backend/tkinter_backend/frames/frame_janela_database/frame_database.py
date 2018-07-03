import os
import tkinter as tk
from ...engine import ttk

from ....constantes import CAMINHO_ICONS_FRAME_INI
from ...frames.frame import frame
from ...box import openfiles,show_info,askyesno
from ...load import load_icons
from ...objetos import frame_informacoes
from ...janelas.janela_add_database.janela_add_database import janela_add_database

from .....processamento import arquivo
from .....processamento.threading import criar_thread
from .....constantes import CAMINHO_METRICAS_DATABASE,\
            CAMINHO_DATABASE,CAMINHO_SELECTED_DATABASE


class frame_database(frame):
    def __init__(self,janela,container):
        frame.__init__(self, janela, "frame_database", container)
        self.icones = load_icons(CAMINHO_ICONS_FRAME_INI, ".png")
        self.iniciar_componentes()

    def update_all_objects(self):
        self.update_databases_box()
        self.update_informations()

    def update_informations(self):
        selected_database_name=self.dataset_box.get()
        selected_database_path=CAMINHO_METRICAS_DATABASE+"//"+selected_database_name+".txt"
        matrics_selected_database=arquivo.abrir_arquivo(selected_database_path)
        array_matrics_selected_database=arquivo.ler_array_arquivo(matrics_selected_database)
        dict_matrics_selected_database=arquivo.converter_array_to_dictonary(array_matrics_selected_database)
        dict_matrics_selected_database.pop("keys_array")

        self.frame_informations.clear_frames()
        self.frame_informations.informacoes=dict_matrics_selected_database
        self.frame_informations.create_frames()

    def update_databases_box(self):
        files_name_list=self.filter_databases()
        selected_database_file=arquivo.abrir_arquivo(CAMINHO_SELECTED_DATABASE)
        selected_database_array=arquivo.ler_array_arquivo(selected_database_file)

        self.dataset_box["value"] = files_name_list
        if(len(files_name_list)==1):
            self.set_config_obj(self.button_exclude,"state","disable")
        else:
            self.set_config_obj(self.button_exclude, "state", "enable")

        if(len(selected_database_array)==1):
            selected_database_name=selected_database_array[0]
            cont=0
            for file_name in files_name_list:
                if(file_name==selected_database_name):
                    self.dataset_box.current(newindex=cont)
                cont=cont+1
        else:
            self.dataset_box.current(newindex=0)


    def iniciar_componentes(self):
        self.pack(fill="both", expand=1)

        self.frame_dataset=tk.Frame(self)
        self.frame_dataset.pack(side=tk.TOP,fill=tk.X)

        self.dataset_box=ttk.Combobox(self.frame_dataset)
        self.dataset_box.pack(side=tk.LEFT,fill=tk.X,expand=1,ipady=9)
        self.dataset_box.config(justify=tk.CENTER)
        self.dataset_box['state'] = 'readonly'
        self.dataset_box.bind('<<ComboboxSelected>>', lambda event: self.update_informations())

        self.button_add = ttk.Button(self.frame_dataset,command=self.adicionar_database)
        self.button_add.pack(side=tk.RIGHT)
        self.button_add.config(image=self.icones["add_database"])

        self.button_exclude=ttk.Button(self.frame_dataset,command=self.remover_database)
        self.button_exclude.pack(side=tk.RIGHT)
        self.button_exclude.config(image=self.icones["remove_database"])

        self.frame_informations=frame_informacoes(self,2,{})
        self.frame_informations.place(relx=0,rely=0.12,relwidth=1,relheight=0.75)

        self.button_confirm=ttk.Button(self,text="Confirmar",command=self.confirm)
        self.button_confirm.pack(anchor=tk.SE,side=tk.BOTTOM)

        self.update_all_objects()

    def filter_databases(self):
        files_name_list=[os.path.splitext(file_name)[0] for file_name in arquivo.list_files(CAMINHO_METRICAS_DATABASE)]
        files_name_list=[file_name for file_name in files_name_list if(arquivo.verificar_arquivo(CAMINHO_DATABASE,file_name))]

        return files_name_list

    def adicionar_database(self):
        janela_add_database(frame_database=self,top_level=self.janela)

    def remover_database(self):
        answer=askyesno("Excluir database","Deseja mesmo excluir essa planilha?",parent=self.janela)
        if(answer):
            chosen_database=self.dataset_box.get()
            selected_database_file=arquivo.abrir_arquivo(CAMINHO_SELECTED_DATABASE)
            selected_database_array=arquivo.ler_array_arquivo(selected_database_file)
            selected_database_name=selected_database_array[0]

            arquivo.deletar_arquivo(CAMINHO_DATABASE,chosen_database)
            arquivo.deletar_arquivo(CAMINHO_METRICAS_DATABASE,chosen_database+".txt")

            if(chosen_database==selected_database_name):
                file=open(CAMINHO_SELECTED_DATABASE,"w")
                file.close()

        self.update_all_objects()


    def confirm(self):
        selected_database=self.dataset_box.get()
        database=arquivo.abrir_arquivo(CAMINHO_SELECTED_DATABASE)
        arquivo.salvar_array_arquivo(database,[selected_database])

        self.janela.destroy()
        criar_thread(self.janela.frame_inicial.carregar_database)


