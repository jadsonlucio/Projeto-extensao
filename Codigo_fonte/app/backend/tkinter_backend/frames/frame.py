import tkinter as tk
from configparser import ConfigParser

from ..engine import eventos
from ..engine import objetos
from ...constantes import CAMINHO_FRAMES_INI


class frame(tk.Frame):

    #gets e sets

    def set_config(self):
        try:
            config=ConfigParser()
            config.read(CAMINHO_FRAMES_INI)
            dirt=dict(config.items(self.nome))
            for key,arg in zip(dirt.keys(),dirt.values()):
                self.set_config_obj(self,key,arg)
        except Exception as e:
            print(str(e))

    def set_config_obj(self, obj, key, value):
        try:
            for child in obj.winfo_children():
                self.set_config_obj(child, key, value)
            obj[key] = value
        except Exception as e:
            print(str(e))

    def __init__(self,janela,nome,container):
        tk.Frame.__init__(self,container)
        self.eventos=eventos(self)
        self.janela=janela
        self.container=container
        self.nome=nome

    def criar_load_bar(self, mode='indeterminate', text_var=None, bar_var=None, bar_maxvalue=0):
        try:
            self.loadbar = objetos.load_frame(self, mode, text_var, bar_var, bar_maxvalue)
        except Exception as e:
            pass

    def limpar_objeto(self,obj):
        try:
            for child in obj.winfo_children():
                child.destroy()
            obj.config(width=0,height=0)
        except Exception as e:
            print(str(e))

    def excluir_objeto(self,obj):
        try:
            for child in obj.winfo_children():
                self.excluir_objeto(child)
            obj.destroy()
        except Exception as e:
            print(str(e))

class frame_container(frame):

    #gets e sets

    def get_frame(self,frame_name):
        try:
            return self.frames[frame_name]
        except Exception as e:
            print(str(e))

    def __init__(self,janela,nome,container):
        frame.__init__(self,janela,nome,container)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(background="red")
        self.frames={}

    def add_frame(self,_frame,frame_name):
        try:
            _frame.grid(row=0,column=0,sticky=tk.NSEW)
            self.frames[frame_name]=_frame
        except Exception as e:
            print(str(e))

    def remove_frame(self,):
        try:
            pass
        except Exception as e:
            print(str(e))

    def show_frame(self,frame_name):
        try:

            self.frame_selecionado=self.frames[frame_name]
            self.frame_selecionado.tkraise()
        except Exception as e:
            print(str(e))