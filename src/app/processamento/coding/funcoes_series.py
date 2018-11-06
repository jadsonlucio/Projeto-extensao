from ...processamento.series_temporais import processamento
from ...libs import estatisticas

#Funcões estatisticas
def tamanho(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.tam(serie)]
        elif(isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.tam(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def soma(serie=None):
    try:
        if (isinstance(serie, list)):
            resultado = ["VALOR", estatisticas.sum(serie)]
        elif(isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.sum(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def maxima(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.maximo(serie)[0]]
        elif (isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.maximo(serie.ploted_data_y)[0]]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def minima(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.minimo(serie)[0]]
        elif (isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.minimo(serie.ploted_data_y)[0]]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def media(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.media(serie)]
        elif (isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.media(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def mediana(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.mediana(serie)]
        elif(isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.mediana(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def moda(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.moda(serie)]
        elif(isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.moda(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def desvio_padrao(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.desvio_padrao(serie)]
        elif(isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.desvio_padrao(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def variancia(serie=None):
    try:
        if(isinstance(serie,list)):
            resultado=["VALOR",estatisticas.variancia(serie)]
        elif(isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.variancia(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def coeficiente_de_variacao(serie=None):
    try:
        if (isinstance(serie, list)):
            resultado = ["VALOR", estatisticas.coeficiente_de_variação(serie)]
        elif (isinstance(serie, processamento.serie_temporal)):
            resultado = ["VALOR", estatisticas.coeficiente_de_variação(serie.ploted_data_y)]
        else:
            return "Erro: Série," + str(serie) + ", inválida."
        return resultado
    except Exception as e:
        return str(e)

def correlacao(serie_1,serie_2):
    try:
        array_1=serie_1
        array_2=serie_2
        if(not (isinstance(serie_1,list) or isinstance(serie_1,processamento.serie_temporal))):
            return "Erro: Série," + str(serie_1) + ", inválida."
        elif(not (isinstance(serie_2,list) or isinstance(serie_2,processamento.serie_temporal))):
            return "Erro: Série," + str(serie_2) + ", inválida."
        if(isinstance(serie_1,processamento.serie_temporal)):
            array_1=serie_1.ploted_data_y
        if(isinstance(serie_2,processamento.serie_temporal)):
            array_2=serie_2.ploted_data_y
        resultado=estatisticas.correlacao(array_1,array_2)
        return ["VALOR",resultado]
    except Exception as e:
        return str(e)

def RMSE(serie_original,serie_prevista):
    try:
        array_1=serie_original
        array_2=serie_prevista
        if(not (isinstance(serie_original,list) or isinstance(serie_original,processamento.serie_temporal))):
            return "Erro: Série," + str(serie_original) + ", inválida."
        elif(not (isinstance(serie_prevista,list) or isinstance(serie_prevista,processamento.serie_temporal))):
            return "Erro: Série," + str(serie_prevista) + ", inválida."
        if(isinstance(serie_original,processamento.serie_temporal)):
            array_1=serie_original.ploted_data_y
        if(isinstance(serie_prevista,processamento.serie_temporal)):
            array_2=serie_prevista.ploted_data_y
        resultado=estatisticas.RMSE(array_1,array_2)
        return ["VALOR",resultado]
    except Exception as e:
        return str(e)

#Funções plot
def plot_serie(serie=None,legenda=None,**plot_args):
    try:
        serie.add_to_processamento()
        if(legenda==None):
            legenda=serie.text_legenda
        if(isinstance(serie,processamento.serie_temporal)):
            serie.plot(label=legenda,**plot_args)
            return ["VALOR",serie]
        else:
            return "Erro: objeto,"+str(serie)+", não é do tipo seriel temporal"
    except Exception as e:
        return str(e)