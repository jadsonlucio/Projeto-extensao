from ...instancias import Instancias
from ...processamento.series_temporais import processamento
from ...processamento.datas import converter_string_to_date

#funções series temporais

def criar_serie_temporal(string):
    try:
        serie_temporal=None
        inst_processamento=processamento.processamento.instancia_selecionada
        nome_serie,data_serie=string.split("->")
        data_inicial,data_final=data_serie.split(",")
        date_inicial=converter_string_to_date(data_inicial,"/")
        date_final=converter_string_to_date(data_final,"/")
        if(date_inicial!=None and date_final!=None):
            pre_processamento=Instancias.get_instancia("pre_processamento")
            keys_array=pre_processamento.keys_array
            for cont in range(0,len(keys_array)):
                if(keys_array[cont]==nome_serie):
                    data_x,data_y=pre_processamento.get_simpletimeserie(date_inicial,date_final,cont)
                    serie_temporal=inst_processamento._criar_serie_temporal(data_x, data_y, date_inicial, date_final, periodo=None,
                                  time_steps=None,text_legenda=None, pai=None, tipo_serie='Normal',ignorar_save=True)
        if(serie_temporal==None):
            return 0
        else:
            return serie_temporal
    except Exception as e:
        print(str(e))
        return 0

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

        return resultado
    except Exception as e:
        return 0