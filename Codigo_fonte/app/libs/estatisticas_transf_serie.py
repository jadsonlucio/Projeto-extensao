from numpy import mean,median,percentile
def reta_tendencia(array_x, array_y):
    soma_x = 0
    soma_x_q = 0
    soma_y = 0
    soma_xy = 0
    x = []
    y = []
    n = len(array_x)
    for cont in range(0, n):
        soma_x = soma_x + array_x[cont]
        soma_x_q = soma_x_q + (array_x[cont] * array_x[cont])
        soma_y = soma_y + array_y[cont]
        soma_xy = soma_xy + (array_x[cont] * array_y[cont])
        x.append(array_x[cont])
    a = ((n * soma_xy) - (soma_x * soma_y)) / (n * soma_x_q - soma_x * soma_x)
    b = (soma_y / n) - a * (soma_x / n)
    for cont in range(0, n):
        y2 = a * array_x[cont] + b
        y.append(y2)
    return x, y

def media_movel_simples(array_x, array_y, lag):
    y1 = []
    x1 = []
    for cont in range(lag, len(array_y)):
        soma = 0
        for cont2 in range(cont - 1, cont - lag - 1, -1):
            soma = soma + array_y[cont2]
        y1.append(soma / lag)
    for cont in range(lag, len(array_x)):
        x1.append(array_x[cont])
    return x1, y1

def variacao(array_x,array_y,quantidade_variacoes=1):
    for cont in range(quantidade_variacoes):
        array_x=array_x[:-1]
        array_y=[array_y[cont]-array_y[cont+1] for cont in range(len(array_y)-1)]
    return array_x,array_y

def ajuste_exponencial(array_x, array_y, w):
    x = []
    y = []
    x.append(array_x[0])
    y.append(array_y[0])
    for cont in range(1, len(array_x)):
        x.append(array_x[cont])
        y_n = w * array_y[cont] + (1 - w) * y[cont - 1]
        y.append(y_n)
    return x, y

def reshape(array_x,array_y,metodo_media,tam_intervalo,repetir_valores=False,**kwargs):
    array_index_x=[]
    array_values_y=[]
    array_values_x=[]
    array_intervalos=[array_y[cont:cont+tam_intervalo] for cont in range(0,len(array_y),tam_intervalo)]
    array_medias=[]
    if(metodo_media=="Média"):
        array_medias=[mean(array) for array in array_intervalos]
    elif(metodo_media=="Médiana"):
        array_medias = [median(array) for array in array_intervalos]
    elif(metodo_media=="Percentil"):
        array_medias =[percentile(array,kwargs["porcentagem"]) for array in array_intervalos]

    if(repetir_valores):
        for valor in array_medias:
            for cont in range(0,tam_intervalo):
                array_values_y.append(valor)
        array_values_x=array_x
        array_values_y=array_values_y[:len(array_y)]
    else:
        array_values_y=array_medias
        index=int(tam_intervalo/2)
        array_values_x=[array_x[index+cont] for cont in range(0,len(array_x),tam_intervalo)]
    return array_values_x,array_values_y

