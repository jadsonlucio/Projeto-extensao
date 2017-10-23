import numpy as np

from numpy import mean,median,sqrt,var,NaN
from statsmodels import api
from . import estatisticas_transf_serie

from ..processamento.exceptions.exception import tratamento_excessao,infoerroexception

# Estatistica basica
def media(array_numeros):
    try:
        return mean(array_numeros)
    except Exception as e:
        tratamento_excessao('Erro')

def media_geometrica(array_numero):
    try:
        multiplicacao=1
        for valor in array_numero:
            multiplicacao=multiplicacao*valor
        return pow(multiplicacao,1/len(array_numero))
    except Exception as e:
        tratamento_excessao("Erro")

def mediana(array_numeros):
    try:
        return median(array_numeros)
    except Exception as e:
        tratamento_excessao('Erro')

def moda(array_numeros):
    try:
        array=[]
        for valor in array_numeros:
            valor_in_array=False
            for valor_array in array:
                if(valor_array[0]==valor):
                    valor_in_array=True
                    valor_array[1]=valor_array[1]+1
            if(valor_in_array==False):
                array.append([valor,1])

        valores_mais_recorrentes=[array[0]]
        for valor_array in array:
            if(valor_array[1]>valores_mais_recorrentes[0][1]):
                valores_mais_recorrentes=[]
                valores_mais_recorrentes.append(valor_array)
            if(valor_array[1]==valores_mais_recorrentes[0][1] and valor_array[0]!=valores_mais_recorrentes[0][0]):
                valores_mais_recorrentes.append(valor_array)
        return valores_mais_recorrentes
    except Exception as e:
        tratamento_excessao('Erro')

def maximo(array_numeros,index_min=None,index_max=None):
    try:
        if(index_min==None):
            index_min=0
        if(index_max==None):
            index_max=len(array_numeros)
        valor_maximo=array_numeros[index_min]
        posicao_valor_maximo=index_min

        for cont in range(index_min,index_max):
            if(valor_maximo<array_numeros[cont]):
                valor_maximo=array_numeros[cont]
                posicao_valor_maximo=cont

        return valor_maximo,posicao_valor_maximo
    except Exception as e:
        tratamento_excessao("Erro")

def minimo(array_numeros, index_min=None, index_max=None):
    try:
        if (index_min == None):
            index_min = 0
        if (index_max == None):
            index_max = len(array_numeros)
        valor_minimo = array_numeros[index_min]
        posicao_valor_minimo = index_min

        for cont in range(index_min, index_max):
            if (valor_minimo > array_numeros[cont]):
                valor_minimo = array_numeros[cont]
                posicao_valor_minimo = cont

        return valor_minimo, posicao_valor_minimo
    except Exception as e:
        tratamento_excessao("Erro")

def amplitude(array_numeros):
    try:
        return maximo(array_numeros)[0]-minimo(array_numeros)[0]
    except Exception as e:
        tratamento_excessao("Erro")

def desvio_padrao(array_numeros):
    try:
        return sqrt(var(array_numeros))
    except Exception as e:
        tratamento_excessao("Erro")

def variancia(array_numeros):
    try:
        return var(array_numeros)
    except Exception as e:
        tratamento_excessao("Erro")

def coeficiente_de_variação(array_numeros):
    try:
        return desvio_padrao(array_numeros)/media(array_numeros)
    except Exception as e:
        tratamento_excessao("Erro")


# Estatistica previsao

def RMSE(serie_original,serie_prevista):
    try:
        erro_quadratico=0
        for valor_original,valor_previsto in zip(serie_original,serie_prevista):
            erro_quadratico=erro_quadratico+(valor_original-valor_previsto)**2
        rmse=sqrt(erro_quadratico/len(serie_prevista))
        return rmse
    except infoerroexception as e:
        tratamento_excessao("Info")
    except Exception as e:
        tratamento_excessao("Erro")

def correlacao(array_x,array_y):
    try:
        return np.corrcoef([array_x,array_y])
    except Exception as e:
        tratamento_excessao("Erro")

def Autocorrelacao(array_numeros,nlags=None,alpha=0.05,**kwargs):
    try:
        if(nlags==None):
            nlags=len(array_numeros)
        array_autocorrelacao=api.tsa.acf(array_numeros,nlags=nlags,alpha=alpha,**kwargs)
        return array_autocorrelacao[0]
    except Exception as e:
        tratamento_excessao("Erro")

def Autocorrelacao_parcial(array_numeros,nlags=None,method="ywm",alpha=0.05,**kwargs):
    try:
        if(nlags==None):
            nlags=len(array_numeros)
        array_autocorrelacao_parcial=api.tsa.pacf(array_numeros,nlags=nlags,method=method,alpha=alpha)
        return array_autocorrelacao_parcial[0]
    except Exception as e:
        tratamento_excessao("Erro")

def Get_best_sazonality(array_numeros,tipo_correlacao="pacf",porcentagem_acuracia=0.05):
    try:
        best_correlacao=None
        best_correlacao_index=None
        if(tipo_correlacao=="pacf"):
            array_autocorrelacao=Autocorrelacao_parcial(array_numeros,nlags=int(len(array_numeros)/2),alpha=porcentagem_acuracia)
        elif(tipo_correlacao=="acf"):
            array_autocorrelacao = Autocorrelacao(array_numeros, nlags=int(len(array_numeros)/2),alpha=porcentagem_acuracia)
        if(porcentagem_acuracia==0.05):
            acuracia=1/sqrt(len(array_numeros))
        cont=0
        for correlacao in array_autocorrelacao:
            if(abs(correlacao)>=acuracia):
                best_correlacao=correlacao
                best_correlacao_index=cont
            cont=cont+1
        print("acuracia"+str(acuracia))
        print("best_correlacao:"+str(best_correlacao)+"index:"+str(best_correlacao_index))

        return best_correlacao,best_correlacao_index

    except Exception as e:
        tratamento_excessao("Erro")

# funcões modificar arrays

def Dimencionar_arrays(arrays, side="right", tamanho=None):
    if (tamanho == None):
        tamanho = min([len(array) for array in arrays])
    new_array = []
    for array in arrays:
        if (side == "right"):
            new_array.append(array[-tamanho:])
        elif (side == "left"):
            new_array.append(array[:tamanho])
    return new_array


def Agrupar_arrays(arrays):
    arrays=Dimencionar_arrays(arrays)
    new_array = []
    [new_array.append([]) for cont in range(0, len(arrays[0]), 1)]
    for array in arrays:
        cont_valor = 0
        for valor in array:
            new_array[cont_valor].append(valor)
            cont_valor = cont_valor + 1
    return new_array

#funções series temporais

def decomposicao_serie(y,frequencia,modelo):
    try:
        if(modelo==0):
            modelo="additive"
        if(modelo==1):
            modelo="multiplicative"
        analise=api.tsa.seasonal_decompose(y,freq=frequencia,model=modelo)
        tendencia=analise.trend
        sasonalidade=analise.seasonal
        ruido=analise.resid
        return tendencia,sasonalidade,ruido
    except Exception as e:
        print(str(e))

def scale_array(array,lim_inferior,lim_superior):
    try:
        new_array=[]
        valor_maximo=maximo(array)[0]
        valor_minimo=minimo(array)[0]
        for valor in array:
            new_value=lim_inferior+lim_superior*((valor-valor_minimo)/(valor_maximo-valor_minimo))
            new_array.append(new_value)

        return new_array
    except Exception as e:
        print(str(e))

def standardize_array(array, mean_array=None, desvio_padrao_array=None):
    try:
        print(array)
        new_array = []
        _media = media(array)
        _desvio_padrao = desvio_padrao(array)
        if (mean_array == None):
            mean_array = media(array)
        if (desvio_padrao_array == None):
            desvio_padrao_array = 1
        for valor in array:
            new_value = (valor - (_media - mean_array)) / (_desvio_padrao / desvio_padrao_array)
            new_array.append(new_value)
        return new_array
    except Exception as e:
        tratamento_excessao("Erro")

# estatisticas de serie

def criar_reletorio_histograma(array,quantidade_classes,round_value=3):
    histograma=[]
    classes=dividir_classe(array,quantidade_classes)
    freq_acumulada=0
    freq_relativa_acumulada=0

    for classe in classes:
        freq=frequencia(array, classe[0], classe[1])
        freq_relativa=freq/len(array)
        freq_acumulada=freq_acumulada+freq
        freq_relativa_acumulada=freq_relativa_acumulada+freq_relativa
        histograma.append({
            "Classe":str(round(classe[0],round_value))+"----|"+str(round(classe[1],round_value)),
            "Ponto Médio":round((classe[0]+classe[1])/2,round_value),
            "Frequência":round(freq,round_value),
            "Frequência Relativa":round(freq_relativa,round_value),
            "Frequência Acumulada":round(freq_acumulada,2),
            "Frequência Relativa Acumulada":round(freq_relativa_acumulada,round_value)
        })
    return histograma

def dividir_classe(array,quantidade_classes):
    maximo_dados=maximo(array)[0]
    minimo_dados=minimo(array)[0]
    amplitudade_dados=amplitude(array)
    amplitude_classes=amplitudade_dados/quantidade_classes
    classes=[]
    for cont in range(quantidade_classes):
        classes.append([minimo_dados+cont*amplitude_classes,minimo_dados+(cont+1)*amplitude_classes])

    return classes

def frequencia(array,valor_minimo,valor_maximo):
    cont_frequencia=0
    for valor in array:
        if(valor>=valor_minimo and valor<valor_maximo):
            cont_frequencia=cont_frequencia+1

    return cont_frequencia