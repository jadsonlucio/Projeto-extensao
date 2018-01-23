import tkinter as tk
from time import sleep
from tkinter import ttk

from ...janelas.janela import janela
from ....constantes import CAMINHO_JANELA_INFO
from .....processamento.threading import criar_thread

BACKGROUND_COLOR="lavender"

class janela_info(janela):
    def __init__(self,titulo="Erro",mensagem_principal="",mensagem_secundaria="",
                                 top_level=True,frames=None,width=300,height=200):
        janela.__init__(self,top_level=top_level,frames=frames)
        self.set_config(CAMINHO_JANELA_INFO)
        self.title(titulo)

        self.overrideredirect(True)
        self.is_visible=True
        self.focus=False

        self.mensagem_principal=mensagem_principal
        self.mensagem_secundario=mensagem_secundaria
        self.width=width
        self.height=height

        self.iniciar_componentes()

    def close_window(self):
        self.destroy()

    def focus_window(self,event):
        self.wm_attributes("-alpha",1)
        self.focus=True
        self.focus_force()

    def move_window(self,event):
        print(event.x,event.y)

    def run_desaparecimento(self,taxa_reducao=0.03,tempo_espera=0.1):
        alpha=1
        while(self.is_visible and self.focus==False):
            self.wm_attributes("-alpha",alpha)
            alpha=alpha-taxa_reducao
            print(alpha)
            if(alpha<=0):
                self.close_window()
                break
            sleep(tempo_espera)

    def iniciar_componentes(self):
        self.frame = tk.Frame(self,width=self.width,height=self.height)
        self.frame.config(background="lavender")
        self.frame.pack_propagate(False)
        self.frame.pack()

        self.close_button=ttk.Button(self.frame,text="x",width=3,command=self.close_window)
        self.close_button.pack(anchor=tk.NE)

        self.text = tk.Label(self.frame, text=self.mensagem_principal,font=("Arial",12,"bold"))
        self.text.config(background=BACKGROUND_COLOR)
        self.text.pack(anchor=tk.CENTER,expand=1)

        self.mais_info_label=tk.Label(self.frame,text="+Mais informações")
        self.mais_info_label.pack(anchor=tk.SW,side=tk.BOTTOM)

        self.frame.bind("<Enter>",self.focus_window)
        self.frame.bind("<B1-Motion>",self.move_window)

        criar_thread(self.run_desaparecimento)

