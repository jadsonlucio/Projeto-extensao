import tkinter as tk

from ....constantes import CAMINHO_JANELA_PARAMETROS
from ...engine import ttk
from ...janelas.janela import janela
from ...frames.frames_janela_parametros import frame_media_movel,\
                        frame_media_exponencial,frame_decomposicao,frame_scale_serie,\
                        frame_medias

class janela_parametros(janela):
    def __init__(self,frames=None,top_level=None):
        janela.__init__(self,top_level,frames)
        self.frame_principal=None
        self.set_config(CAMINHO_JANELA_PARAMETROS)
        self.wm_attributes("-toolwindow",True)
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
        if (tipo_parametro=="SCALE"):
            self.frame_principal = frame_scale_serie.frame_scale_serie(self,self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal],["frame_principal"])
        if (tipo_parametro=="MEDIAS"):
            self.frame_principal = frame_medias.frame_medias(self,self)
            self.frame_principal.iniciar_componentes()
            self.add_frames([self.frame_principal], ["frame_principal"])
        if (tipo_parametro=="AUTOCORRELACAO"):
            elf.frame_principal = frame_medias.frame_medias(self, self)
            self.frame_principal.iniciar_componentes()

