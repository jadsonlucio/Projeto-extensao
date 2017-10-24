import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento


class frame_boxplot(frame):
    def __init__(self, janela, container):
        frame.__init__(self, janela, "frame_boxplot", container)

    def func_aplicar(self, **kwargs):
        try:
            time_steps = int(self.text_time_steps.get())
            periodo = self.periodo_dirt[self.box_periodo.get()]
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()[:]
            for serie in series_selecionadas:
                if(serie!=series_selecionadas[-1]):
                    inst_processamento.processamento_plot.box_plot(serie,periodo,time_steps,update_screen=False)
                else:
                    inst_processamento.processamento_plot.box_plot(serie, periodo, time_steps, update_screen=True)
        except Exception as e:
            print(str(e))


    def iniciar_componentes(self):
        try:

            self.label_periodo = tk.Label(self, text="Escolha o periodo")
            self.label_periodo.pack()

            self.frame_params_periodo = tk.Frame(self)
            self.frame_params_periodo.pack()

            self.text_time_steps = tk.Entry(self.frame_params_periodo)
            self.text_time_steps.config(width=5)
            self.text_time_steps.grid(row=0, column=0, sticky=tk.W)

            self.periodo_dirt = {"minuto(s)": "minuto",
                                 "hora(s)": "hora",
                                 "dia(s)": "dia"}
            self.box_periodo = ttk.Combobox(self.frame_params_periodo)
            self.box_periodo.config(justify=tk.CENTER, width=8)
            self.box_periodo["value"] = ["minuto(s)", "hora(s)", "dia(s)"]
            self.box_periodo['state'] = 'readonly'
            self.box_periodo.current(newindex=0)
            self.box_periodo.grid(row=0, column=1)

            self.botao_cancelar = tk.Button(self, text="Cancelar", command=lambda: self.janela.destroy())
            self.botao_aplicar = tk.Button(self, text="Aplicar", command=self.func_aplicar)

            self.botao_cancelar.pack()
            self.botao_aplicar.pack()
        except Exception as e:
            print(str(e))

