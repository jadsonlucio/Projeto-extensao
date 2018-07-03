import tkinter as tk
from ...engine import ttk

from ....constantes import CAMINHO_ICONS_FRAME_INI
from ...frames.frame import frame
from ...load import load_icons

from .....instancias.Instancias import get_instancia
from .....processamento.threading import criar_thread
from ...janelas.janela_database.janela_database import janela_database
from ...janelas.janela_add_database.janela_add_database import janela_add_database

class frame_inicial(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_inicial",container)
        self.janela=janela
        self.container=container
        self.icones=load_icons(CAMINHO_ICONS_FRAME_INI,".png")
        self.database=get_instancia("database")
        self.set_config()
        self.iniciar_componentes()

    def iniciar_componentes(self):
        try:
            self.label_inicio = tk.Label(self, text="Inicio", font=('Arial', '40'))
            self.label_inicio.pack(anchor=tk.W, padx=45, pady=30)
            self.frame_erro = None
            if(not self.database.verificar_arquivo()):
                self.frame_erro = frame(self.janela, 'frame_erro', self)
                self.frame_erro.pack(anchor=tk.W, padx=60)
                self.botao_criar = ttk.Button(self.frame_erro, text="Criar base de dados",
                                              command=self.adicionar_database)
                self.botao_criar.config(image=self.icones['create'])
                self.botao_criar.pack(side=tk.LEFT, padx=40)
                self.label_info = ttk.Label(self.frame_erro, text="Notamos que não existe uma base de dados.\n"
                                                                  "Se esta for sua primeira vez, favor\n"
                                                                  "toque para adicionar a planilha com os dados.",
                                            font=('Segoe UI', '20'))
                self.label_info.pack(side=tk.LEFT)

            self.label_menu = ttk.Label(self, text="Menu", font=('Quaterback Fight', '24'))
            self.label_menu.pack(anchor=tk.W, padx=48, pady=50)
            self.frame_menu = frame(self.janela, 'frame_menu', self)
            self.frame_menu.pack(anchor=tk.W, padx=83)
            self.botao_adicionar = ttk.Button(self.frame_menu, text="Adicionar dados",
                                              command=self.gerenciar_database)
            self.botao_adicionar.config(image=self.icones['add'])
            self.botao_adicionar.grid(row=0, column=0, padx=10)
            self.botao_adicionar_texto = ttk.Label(self.frame_menu, text="Gerenciar base de dados")
            self.botao_adicionar_texto.grid(row=1, column=0)
            self.botao_draw = ttk.Button(self.frame_menu, text="Desenhar gráficos", command=self.go_draw)
            self.botao_draw.config(image=self.icones['desenhar'])
            self.botao_draw.grid(row=0, column=1, padx=10)
            self.botao_adicionar_texto = ttk.Label(self.frame_menu, text="Desenhar gráficos")
            self.botao_adicionar_texto.grid(row=1, column=1)

            if (not self.database.verificar_arquivo()):
                self.frame_menu.set_config_obj(self.frame_menu, 'state', 'disabled')
            else:
                self.frame_menu.set_config_obj(self.frame_menu, 'state', 'disabled')
                self.database.carregar_database()
                self.janela.after(0, criar_thread(self.carregar_database))
        except Exception as e:
            print(str(e))

    def carregar_database(self):
        try:
            self.set_config_obj(self.frame_menu,"state","disable")
            text_var = tk.StringVar()
            bar_var = tk.DoubleVar()
            self.criar_load_bar(mode='indeterminado', text_var=text_var, bar_var=bar_var)
            self.loadbar.show_load()
            self.loadbar.pack(side=tk.BOTTOM, fill=tk.X)
            self.database.carregar_database()
            self.set_config_obj(self.frame_menu, 'state', 'normal')
            self.loadbar.hide_load()
            self.set_config_obj(self.frame_menu, "state", "enable")
        except Exception as e:
            self.carregar_database()

    def gerenciar_database(self):
        try:
            self.set_config_obj(self.frame_menu,"state","disabled")
            janela_database(self,top_level=self.janela)
        except Exception as e:
            print(str(e))

    def adicionar_database(self):
        try:
            self.set_config_obj(self.frame_erro, 'state', 'disabled')
            janela_add_database(self,top_level=self.janela)
        except Exception as e:
            print(str(e))

    def go_draw(self):
        self.janela.show_frame("frame_desenho")