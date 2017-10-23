import tkinter as tk
from ...engine import ttk
from ...frames.frame import frame

from .....processamento.series_temporais.processamento import processamento

class frame_normalise_serie(frame):
    def __init__(self,janela,container):
        frame.__init__(self,janela,"frame_normalise",container)

    def func_aplicar(self):
        try:
            tipo_normalizacao=self.box_tipo_normalizacao.get()
            inst_processamento = processamento.instancia_selecionada
            series_selecionadas = inst_processamento.get_series_selecionadas()
            for serie_temporal in series_selecionadas:
                if (tipo_normalizacao == "Reescala"):
                    limite_superior = float(self.text_lim_superior.get())
                    limite_inferior = float(self.text_lim_inferior.get())
                    serie_temporal.scale_serie(lim_inferior=limite_inferior,lim_superior=limite_superior)
                elif(tipo_normalizacao== "Padronização"):
                    media=float(self.text_media.get())
                    desvio_padrao=float(self.text_desvio_padrao.get())
                    serie_temporal.standardize_serie(media,desvio_padrao)
                serie_temporal.plot(label=serie_temporal.text_legenda)
            self.janela.destroy()
        except Exception as e:
            print(str(e))

    def atualizar_frame_normalizacao(self,event=None):
        try:
            self.limpar_objeto(self.frame_params_normalizacao)
            if(self.box_tipo_normalizacao.get()=="Reescala"):
                self.label_lim_superior = tk.Label(self.frame_params_normalizacao, text="Digite o limite superior")
                self.label_lim_superior.pack()
                self.text_lim_superior = tk.Entry(self.frame_params_normalizacao)
                self.text_lim_superior.pack()
                self.label_lim_inferior = tk.Label(self.frame_params_normalizacao, text="Digite o limite inferior")
                self.label_lim_inferior.pack()
                self.text_lim_inferior = tk.Entry(self.frame_params_normalizacao)
                self.text_lim_inferior.pack()
            if(self.box_tipo_normalizacao.get()=="Padronização"):
                self.label_media = tk.Label(self.frame_params_normalizacao, text="Digite a media")
                self.label_media.pack()
                self.text_media = tk.Entry(self.frame_params_normalizacao)
                self.text_media.pack()
                self.label_desvio_padrao = tk.Label(self.frame_params_normalizacao, text="Digite o desvio padrão")
                self.label_desvio_padrao.pack()
                self.text_desvio_padrao = tk.Entry(self.frame_params_normalizacao)
                self.text_desvio_padrao.pack()

        except Exception as e:
            print(str(e))

    def iniciar_componentes(self):
        try:
            self.text_tipo_normalizacao=tk.Label(self,text="Selecione o tipo de normalização")
            self.text_tipo_normalizacao.pack()
            self.box_tipo_normalizacao=ttk.Combobox(self)
            self.box_tipo_normalizacao["value"]=["Reescala","Padronização"]
            self.box_tipo_normalizacao["state"]="readonly"
            self.box_tipo_normalizacao.current(newindex=0)
            self.box_tipo_normalizacao.pack()
            self.box_tipo_normalizacao.bind("<<ComboboxSelected>>", self.atualizar_frame_normalizacao)

            self.frame_params_normalizacao=tk.Frame(self)
            self.frame_params_normalizacao.pack()

            self.botao_cancelar=tk.Button(self,text="Cancelar",command=lambda:self.janela.destroy())
            self.botao_aplicar=tk.Button(self,text="Aplicar",command=self.func_aplicar)

            self.botao_cancelar.pack()
            self.botao_aplicar.pack()

            self.atualizar_frame_normalizacao()
        except Exception as e:
            print(str(e))

