from ...processamento.series_temporais import processamento
from ...libs import estatisticas

# Variaveis globais
kwargs_subplots_fill={}

def fill_between(serie_temporal,divisor=0,limpar=True,**plot_args):
    try:
        if(not isinstance(serie_temporal,processamento.serie_temporal)):
            return "Erro: objeto," + str(serie_temporal) + ", não é do tipo seriel temporal"
        instancia_processamento=processamento.get_instancia_selecionada()
        figura,subplot=instancia_processamento.processamento_plot.plot_area(serie_temporal,divisor,update_screen=True,**plot_args)
        if(limpar==True):
            for key in kwargs_subplots_fill.keys():
                if(key==subplot):
                    for figura in kwargs_subplots_fill[key]:
                        figura.remove()
                    kwargs_subplots_fill[key]=[]
        encontrou_subplot=False
        for key in kwargs_subplots_fill.keys():
            if(key==subplot):
                encontrou_subplot=True
        if(not encontrou_subplot):
            kwargs_subplots_fill[subplot]=[]
        kwargs_subplots_fill[subplot].append(figura)

        return ["VALOR",serie_temporal]
    except Exception as e:
        return str(e)
