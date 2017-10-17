import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento

class frame_correlacao(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_correlacao",container)

    def func_aplicar(self):
        try:
            limite_superior=float(self.text_lim_superior.get())
            limite_inferior=float(self.text_lim_inferior.get())
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()
            for serie_temporal in series_selecionadas:
                serie_temporal.scale_serie(lim_inferior=limite_inferior,lim_superior=limite_superior)
                serie_temporal.plot(label=serie_temporal.text_legenda)
            self.janela.destroy()
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.label_lim_superior=tk.Label(self,text="Digite o limite superior")
            self.label_lim_superior.pack()
            self.text_lim_superior=tk.Entry(self)
            self.text_lim_superior.pack()
            self.label_lim_inferior = tk.Label(self,text="Digite o limite inferior")
            self.label_lim_inferior.pack()
            self.text_lim_inferior = tk.Entry(self)
            self.text_lim_inferior.pack()

            self.botao_cancelar=tk.Button(self,text="Cancelar",command=lambda:self.janela.destroy())
            self.botao_aplicar=tk.Button(self,text="Aplicar",command=self.func_aplicar)

            self.botao_cancelar.pack()
            self.botao_aplicar.pack()
        except Exception as e:
            print(str(e))

