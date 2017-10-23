import tkinter as tk

from ....constantes import CAMINHO_JANELA_PARAMETROS
from ...engine import ttk
from ...janelas.janela import janela
from ...frames.frames_janela_parametros import frame_media_movel,\
                        frame_media_exponencial,frame_decomposicao,frame_normalise_serie,\
                        frame_medias,frame_autocorrelacao,frame_correlacao,frame_histograma


class janela_parametros(janela):
    def __init__(self,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.frame_principal=None
        self.set_config(CAMINHO_JANELA_PARAMETROS)
        self.wm_attributes("-toolwindow",True)
        self.resizable(0,0)
        self.focus_force()
        self.grab_set()

    def iniciar_componentes(self,tipo_parametro):
        if(tipo_parametro=="MMS"):
            self.frame_principal=frame_media_movel.frame_media_movel(self,self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal],["frame_principal"])
        if (tipo_parametro == "MME"):
            self.frame_principal = frame_media_exponencial.frame_media_exponencial(self, self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal], ["frame_principal"])
        if (tipo_parametro=="DECOMPOSICAO"):
            self.frame_principal = frame_decomposicao.frame_decomposicao(self, self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal], ["frame_principal"])
        if (tipo_parametro=="NORMALIZAR"):
            self.frame_principal = frame_normalise_serie.frame_normalise_serie(self,self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal],["frame_principal"])
        if (tipo_parametro=="MEDIAS"):
            self.frame_principal = frame_medias.frame_medias(self,self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal], ["frame_principal"])
        if (tipo_parametro=="AUTOCORRELACAO"):
            self.frame_principal = frame_autocorrelacao.frame_autocorrelacao(self, self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal], ["frame_principal"])
        if(tipo_parametro=="HISTOGRAMA"):
            self.frame_principal = frame_histograma.frame_histograma(self, self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal], ["frame_principal"])
        if(tipo_parametro=="CORRELACAO"):
            self.frame_principal = frame_correlacao.frame_correlacao(self, self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal], ["frame_principal"])
