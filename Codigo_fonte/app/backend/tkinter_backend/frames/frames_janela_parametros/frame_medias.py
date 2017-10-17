import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento

class frame_medias(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_medias",container)

    def func_aplicar(self):
        try:
            metodo_media=self.box_tipo_localidade.get()
            repetir_valores=self.repetir_valores_var.get()
            time_steps=int(self.text_time_steps.get())
            periodo=self.periodo_dirt[self.box_periodo.get()]
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()
            for serie in series_selecionadas:
                periodo_convertido=int(serie.converter_tempo(periodo,time_steps))
                serie.reshape_serie(metodo_media,periodo_convertido,repetir_valores)
                serie.plot(label=serie.text_legenda)
        except Exception as e:
            print(str(e))

    def atualizar_frame_localidade(self,event):
        try:
            self.limpar_objeto(self.frame_params_tipo_localidade)
            if(self.box_tipo_localidade.get()=="Percentil"):
                self.label_porcentagem=tk.Label(self.frame_params_tipo_localidade,text="Porcentagem:")
                self.label_porcentagem.pack()
                self.text_porcentagem=tk.Entry(self.frame_params_tipo_localidade)
                self.text_porcentagem.pack()
        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.label_tipo_localidade=tk.Label(self,text="Digite o método de localidade")
            self.label_tipo_localidade.pack()
            self.box_tipo_localidade=ttk.Combobox(self)
            self.box_tipo_localidade["value"]=["Média","Médiana","Percentil"]
            self.box_tipo_localidade['state'] = 'readonly'
            self.box_tipo_localidade.current(newindex=0)
            self.box_tipo_localidade.pack()
            self.box_tipo_localidade.bind("<<ComboboxSelected>>", self.atualizar_frame_localidade)

            self.frame_params_tipo_localidade=tk.Frame(self)
            self.frame_params_tipo_localidade.config(background="gainsboro")
            self.frame_params_tipo_localidade.pack()

            self.frame_params_periodo=tk.Frame(self)
            self.frame_params_periodo.pack()

            self.label_periodo = tk.Label(self,text="Escolha o periodo")
            self.label_periodo.pack()

            self.frame_params_periodo=tk.Frame(self)
            self.frame_params_periodo.pack()

            self.text_time_steps= tk.Entry(self.frame_params_periodo)
            self.text_time_steps.config(width=5)
            self.text_time_steps.grid(row=0,column=0,sticky=tk.W)

            self.periodo_dirt={"minuto(s)":"minuto",
                               "hora(s)":"hora",
                               "dia(s)":"dia"}
            self.box_periodo=ttk.Combobox(self.frame_params_periodo)
            self.box_periodo.config(justify=tk.CENTER, width=8)
            self.box_periodo["value"]=["minuto(s)","hora(s)","dia(s)"]
            self.box_periodo['state'] = 'readonly'
            self.box_periodo.current(newindex=0)
            self.box_periodo.grid(row=0,column=1)
            
            self.repetir_valores_var=tk.IntVar()
            self.repetir_valores_check=tk.Checkbutton(self,text="Repetir valores",variable=self.repetir_valores_var)
            self.repetir_valores_check.pack(anchor=tk.W)

            self.botao_cancelar=tk.Button(self,text="Cancelar",command=lambda:self.janela.destroy())
            self.botao_aplicar=tk.Button(self,text="Aplicar",command=self.func_aplicar)

            self.botao_cancelar.pack()
            self.botao_aplicar.pack()
        except Exception as e:
            print(str(e))

