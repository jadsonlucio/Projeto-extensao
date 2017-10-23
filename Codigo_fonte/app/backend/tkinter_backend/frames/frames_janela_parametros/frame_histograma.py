import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento


class frame_histograma(frame):
    def __init__(self, janela, container):
        frame.__init__(self, janela, "frame_histograma", container)

    def func_aplicar(self, **kwargs):
        try:
            quantidade_classes=int(self.quantidade_classes.get())
            normalizar_dados=self.normalizar_dados_var.get()
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()
            for serie in series_selecionadas:
                if(serie!=series_selecionadas[-1]):
                    update_screen=False
                else:
                    update_screen=True
                inst_processamento.processamento_plot.plot_histograma(serie, quantidade_classes, normalizar_dados,update_screen)
        except Exception as e:
            print(str(e))


    def iniciar_componentes(self):
        try:
            self.text_quantidade_classes=tk.Label(self,text="Digite a quantidade de classes")
            self.text_quantidade_classes.pack()
            self.quantidade_classes=tk.Entry(self)
            self.quantidade_classes.pack()

            self.normalizar_dados_var=tk.IntVar()
            self.normalizar_dados=tk.Checkbutton(self,text="Normalizar",variable=self.normalizar_dados_var)
            self.normalizar_dados.pack()

            self.botao_cancelar = tk.Button(self, text="Cancelar", command=lambda: self.janela.destroy())
            self.botao_aplicar = tk.Button(self, text="Aplicar", command=self.func_aplicar)

            self.botao_cancelar.pack()
            self.botao_aplicar.pack()
        except Exception as e:
            print(str(e))

