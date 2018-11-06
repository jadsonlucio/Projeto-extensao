from ...instancias import Instancias
from ...processamento.series_temporais import processamento
from ...processamento.datas import converter_string_to_date,month_range,timedelta
from ...libs.estatisticas import np
from . import funcoes_series,funcoes_desenho,funcoes_janelas
funcoes_names={
    funcoes_series.tamanho:["tam","tamanho","len"],
    funcoes_series.soma:["sum","soma"],
    funcoes_series.mediana:["mediana","median"],
    funcoes_series.media:["media","mean"],
    funcoes_series.maxima:["maxima","max"],
    funcoes_series.minima:["minima","min"],
    funcoes_series.desvio_padrao:["desvio_padrao","d_p"],
    funcoes_series.variancia:["variancia","var"],
    funcoes_series.coeficiente_de_variacao:["coef_var","coeficiente_variacao"],
    funcoes_series.correlacao:["correlacao","corr"],
    funcoes_series.RMSE:["rmse","RMSE"],
    funcoes_series.plot_serie:["plot_serie","plot","desenhar"],

    funcoes_desenho.fill_between:["fill_serie"],

    funcoes_janelas.criar_tabela_series:["criar_tabela_series","criar_tabela_serie"],
    funcoes_janelas.criar_janela_help:["help","ajuda"],

}


kwargs_funcoes={}

# Criar base de funcões

def criar_kwargs_funcoes():
    for func in funcoes_names.keys():
        for key_func in funcoes_names[func]:
            kwargs_funcoes[key_func]=func

criar_kwargs_funcoes()

#funções series temporais

def converter_data_serie(data_serie):
    try:
        array_data = data_serie.split(";")
        if (len(array_data) == 1):
            data_string = array_data[0]
            data = data_string.split("/")
            if (len(data) == 2):
                data_inicial = converter_string_to_date(data_string, "/")
                tamanho_mes=month_range(mes=data_inicial.day, ano=data_inicial.year)[1]
                data_final = data_inicial + timedelta(days=tamanho_mes)
            elif (len(data) == 3):
                data_inicial = converter_string_to_date(data_string, "/")
                data_final = data_inicial + timedelta(days=1)
            else:
                return "Erro na data da serie:" + data_serie
        elif(len(array_data)==2):
            data_inicial=converter_string_to_date(array_data[0],"/")
            data_final=converter_string_to_date(array_data[1],"/")
        else:
            return "Número de ; acima de 1"
        return data_inicial,data_final
    except Exception as e:
        return str(e)

def criar_serie_temporal(string):
    try:
        serie_temporal=None
        inst_processamento=processamento.processamento.instancia_selecionada
        nome_serie,data_serie=string.split("->")
        data_inicial=None
        data_final=None
        array_datas=converter_data_serie(data_serie)
        if(isinstance(array_datas,str)):
            return array_datas
        elif(len(array_datas)==2):
            data_inicial,data_final=array_datas
        if(data_inicial!=None and data_final!=None):
            pre_processamento=Instancias.get_instancia("pre_processamento")
            keys_array=pre_processamento.keys_array
            for cont in range(0,len(keys_array)):
                if(keys_array[cont]==nome_serie):
                    data_x,data_y=inst_processamento._get_serie_data(data_inicial,data_final,cont)
                    serie_temporal=inst_processamento._criar_serie_temporal(data_x, data_y, data_inicial, data_final, periodo=None,
                                  time_steps=None,text_legenda=nome_serie, pai=None, tipo_serie='Normal',ignorar_save=True)
        if(serie_temporal==None):
            return 0
        else:
            return serie_temporal
    except Exception as e:
        return str(e)

def pegar_serie_temporal(string):
    try:
        index=int(string.replace(":",""))
        return get_serie_by_index(index)
    except Exception as e:
        return str(e)

def get_serie_by_index(index_serie):
    try:
        cont=0
        for isntancia in processamento.instancias_processamento:
            for serie in isntancia.series_temporais:
                if(cont==index_serie):
                    return serie
                cont=cont+1
        return 0
    except Exception as e:
        print(str(e))

def get_type_obj(obj):
    if (isinstance(obj, str)):
        return "STRING"
    elif (isinstance(obj, int) or isinstance(obj, float)):
        return "VALOR"
    else:
       return "VALOR"

#funções conversão

def converter_string_inteiro(string):
    try:
        resultado=int(string)
        return resultado
    except Exception as e:
        return -1

def converter_string_array_float(string,separador=','):
    try:
        array_float=[float(valor) for valor in string.split(separador)]
        return array_float
    except Exception as e:
        return 0

#funções aritmeticas

def operacao_aritmetica(valor_1,operador,valor_2):
    try:
        resultado=None
        if(isinstance(valor_1,list)):
            valor_1=np.array(valor_1)
        if(isinstance(valor_2,list)):
            valor_2=np.array(valor_2)
        if(isinstance(valor_2,processamento.serie_temporal)):
            copia=valor_1
            valor_1=valor_2
            valor_2=copia
        if(operador=="+"):
            resultado=valor_1+valor_2
        elif(operador=="-"):
            resultado = valor_1 - valor_2
        elif(operador=="/"):
            resultado = valor_1 / valor_2
        elif(operador=="*"):
            resultado = valor_1 * valor_2
        elif(operador=="^"):
            resultado = valor_1**valor_2
        if(isinstance(resultado,np.ndarray)):
            resultado=[valor for valor in resultado]
        return resultado
    except Exception as e:
        print(str(e))
        return str(e)