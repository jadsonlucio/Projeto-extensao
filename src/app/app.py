from .backend import backend_selecionado
from .processamento.tabela import criar_instancia_database
from .processamento.series_temporais.pre_processamento import criar_instancia_pre_processamento

# Variaveis globais
database=None
pre_processamento=None
processamento=None


# Função rodar app
def run():
    global database,pre_processamento
    database=criar_instancia_database()
    pre_processamento=criar_instancia_pre_processamento()
    janela=backend_selecionado.janelas.janela_inicial.janela_inicial.janela_inicial(None,None)
    janela.iniciar_componentes()
    frame=backend_selecionado.frames.frames_janela_principal.frame_inicial.frame_inicial(janela,janela.container)
    frame2 = backend_selecionado.frames.frames_janela_principal.frame_desenho.frame_desenho(janela, janela.container)
    janela.add_frames([frame,frame2],["frame_inicial","frame_desenho"])
    janela.show_frame("frame_inicial")
    janela.mainloop()

class aplicacao():
    def __init__(self):
        pass
