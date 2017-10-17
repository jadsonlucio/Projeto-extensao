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

def Autocorrelacao(array_numeros,nlags=None,**kwargs):
    try:
        if(nlags==None):
            nlags=len(array_numeros)
        array_autocorrelacao=api.tsa.acf(array_numeros,**kwargs)
        return array_autocorrelacao
    except Exception as e:
        tratamento_excessao("Erro")

def Autocorrelacao_parcial(array_numeros,nlags=None,**kwargs):
    try:
        if(nlags==None):
            nlags=len(array_numeros)
        array_autocorrelacao_parcial=api.tsa.pacf(array_numeros,nlags=nlags)
        return array_autocorrelacao_parcial
    except Exception as e:
        tratamento_excessao("Erro")

def Get_best_sazonality(array_numeros,tipo_correlacao="pacf",porcentagem_acuracia="95%"):
    try:
        best_correlacao=None
        best_correlacao_index=None
        if(tipo_correlacao=="pacf"):
            array_autocorrelacao=Autocorrelacao_parcial(array_numeros,nlags=int(len(array_numeros)/2))
        elif(tipo_correlacao=="acf"):
            array_autocorrelacao = Autocorrelacao(array_numeros, nlags=int(len(array_numeros)/2))
        if(porcentagem_acuracia=="95%"):
            acuracia=1/sqrt(len(array_numeros))*2
        cont=0
        for correlacao in array_autocorrelacao:
            if(correlacao>=acuracia):
                best_correlacao=correlacao
                best_correlacao_index=cont
            cont=cont+1
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