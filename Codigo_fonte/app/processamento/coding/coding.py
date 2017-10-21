from ...processamento.series_temporais.series_temporais import serie_temporal
from .tratamento_codigo import buscar_simbolo_aritmetico,buscar_simbolo_contencao,\
             buscar_simbolos_numericos,buscar_simbolos_series,buscar_nomes_funcoes,\
             buscar_simbolos_separacao,buscar_simbolo_string
from . import funcoes
from .simbolos import SIMBOLOS_SERIES_TEMPORAIS,SIMBOLOS_ARITIMETICOS,SIMBOLOS_CONTENCAO,SIMBOLOS_FUNCOES,SIMBOLOS_SEPARACAO

dirt_variaveis={}

def run_code(array_objetos,array_tipos):
    try:
        if(len(array_objetos)!=len(array_tipos)):
            return "Um erro inesperado aconteceu"
        while (len(array_objetos) != 1):
            cont=0
            for cont in range(0,len(array_objetos)):
                if(isinstance(array_objetos[cont],str)):
                    if(array_objetos[cont]==")"):
                        for cont2 in range(cont,0,-1):
                            if(array_objetos[cont2]=="("):
                                run_code_entre(array_objetos,cont2,cont)

    except Exception as e:
        print(str(e))

def run_code_entre(array_objetos,array_tipos,inicio,fim):
    try:
        objetos=array_objetos[inicio:fim]
        objetos_tipo=array_tipos[inicio:fim]
        for simbolo in SIMBOLOS_ARITIMETICOS:
            for cont in range(len(objetos)):
                if(objetos_tipo[cont]=="ARITMETICO" and objetos_tipo[cont-1]==""):
                    pass
    except Exception as e:
        print(str(e))


def decode_code(string):
    try:
        variavel=None
        array_objetos=None
        if("=" in string):
            variavel,string=string.split("=")
        codigo_tratado=tratar_codigo(string)
        if(len(codigo_tratado)!=0):
            array_objetos=sintaxe_analise(codigo_tratado)
        else:
            return "Nenhum texto digitado"
        return array_objetos
    except Exception as e:
        return 0

def buscar_variaveis(string,cont,array_objetos):
    try:
        soma_cont = 0
        for key in dirt_variaveis.keys():
            if(string[cont:len(key)]==key):
                array_objetos.append(dirt_variaveis[key])
                soma_cont=soma_cont+len(key)
                break;
        cont=cont+soma_cont
        return cont,array_objetos
    except Exception as e:
        print("buscar_variaveis")

def sintaxe_analise(string):
    try:
        array_objetos=[]
        array_funcoes_procura=[buscar_simbolo_aritmetico,buscar_simbolo_contencao,
                               buscar_simbolos_series,buscar_simbolos_numericos,
                               buscar_nomes_funcoes,buscar_variaveis,buscar_simbolos_separacao,
                               buscar_simbolo_string]
        achou_erro=False
        cont=0
        while(cont<len(string)):
            valor_erro=len(array_objetos)
            for func_procura in array_funcoes_procura:
                cont,array_objetos=func_procura(string,cont,array_objetos)
                if(cont>=len(string)):
                    break;
            if(len(array_objetos)==valor_erro):
                achou_erro=True
                break;
        if(achou_erro):
            return cont
        else:
            return array_objetos
    except Exception as e:
        return 0

def semantica_analise(array_objetos):
    try:
        cont=0
        array_resultados=[]
        cont_1=0
        cont_2=0
        for obj in array_objetos:
            if(isinstance(obj,str)):
                if(obj=="("):
                    cont_1=cont_1+1
                if(obj==")"):
                    cont_2=cont_2+1
        if(cont_1!=cont_2):
            return "Numero parênteses incorreto"


        return array_objetos
    except Exception as e:
        print("semantica_analise")


def tratar_codigo(string):
    try:
        new_code=""
        for char in string:
            if(char!=' ' or char != '\n'):
                new_code=new_code+char
        return new_code[:-1]
    except Exception as e:
        return 0

def tratar_objetos(array_objetos):
    try:
        for cont_objetos in range(0,len(array_objetos)):
            if(array_objetos[cont_objetos][0]=="ARRAY"):
                tratar_array(array_objetos[cont_objetos][1])
    except Exception as e:
        return 0

def tratar_array(array):
    try:
        for obj in array:
            if(obj[0]=="ARRAY"):
                tratar_array(obj[1])
            elif(obj[0]=="VALOR"):
                objeto=tratar_array_text(obj[1])
    except Exception as e:
        return 0

def tratar_array_text(string):
    resultado=None
    if("," in string):
        array_string=string.split(",")
        for text in array_string:
            pass
    else:
        pass
