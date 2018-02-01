from . import tratamento_codigo
from .simbolos import SIMBOLOS_SERIES_TEMPORAIS, SIMBOLOS_ARITIMETICOS, SIMBOLOS_CONTENCAO, SIMBOLOS_FUNCOES, \
    SIMBOLOS_SEPARACAO
import sys, os

dirt_variaveis = {}


def run_code(array_objetos):
    try:
        while (True):
            new_array_objetos = array_objetos[:]
            array_objetos = run_all_operations(array_objetos)
            if(not isinstance(array_objetos,list)):
                return array_objetos
            array_objetos = run_all_functions(array_objetos)
            if(not isinstance(array_objetos,list)):
                return array_objetos
            array_objetos = run_verificacao(array_objetos)
            if(not isinstance(array_objetos,list)):
                return array_objetos
            if (len(new_array_objetos) == len(array_objetos)):
                break;
        return array_objetos

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def run_code_entre(array_objetos, array_tipos, inicio, fim):
    try:
        objetos = array_objetos[inicio:fim]
        objetos_tipo = array_tipos[inicio:fim]
        for simbolo in SIMBOLOS_ARITIMETICOS:
            for cont in range(len(objetos)):
                if (objetos_tipo[cont] == "ARITMETICO" and objetos_tipo[cont - 1] == ""):
                    pass
    except Exception as e:
        print(str(e))


def run_all_operations(array_objetos):
    for simbolo_aritimetico in SIMBOLOS_ARITIMETICOS:
        array_objetos = run_operacoes(array_objetos, simbolo_aritimetico)
        if(not isinstance(array_objetos,list)):
            return array_objetos

    return array_objetos

def run_all_functions(array_objetos):
    try:
        cont_obj=0
        while(cont_obj<len(array_objetos)):
            if(array_objetos[cont_obj][0]=="FUNCAO"):
                nome_funcao=array_objetos[cont_obj][1]
                array_objetos=run_function(nome_funcao,cont_obj,array_objetos)
                if(not isinstance(array_objetos,list)):
                    return array_objetos
            cont_obj=cont_obj+1
        return array_objetos
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))

def run_verificacao(array_objetos):
    cont_obj=1
    while(cont_obj<len(array_objetos)-1):
        if(array_objetos[cont_obj-1][0]=="CONTENCAO" and array_objetos[cont_obj+1][0]=="CONTENCAO"):
            array_objetos.remove(array_objetos[cont_obj+1])
            array_objetos.remove(array_objetos[cont_obj-1])

        cont_obj=cont_obj+1
    return array_objetos

def run_function(funcao_name,cont,array_objetos):
    try:
        args_parameters = []
        kargs_parameters = {}
        quant_parenteses_1 = 0
        quant_parenteses_2 = 0
        cont_2 = cont+1
        while (cont_2 < len(array_objetos)):
            if (array_objetos[cont_2][0] != "VALOR" and array_objetos[cont_2][0] != "ARRAY" and
                        array_objetos[cont_2][0] != "KWARG" and array_objetos[cont_2][0] != "SEPARACAO"
                and array_objetos[cont_2][0] != "STRING" and array_objetos[cont_2][0] != "CONTENCAO"):
                break
            if(array_objetos[cont_2][1]=="("):
                quant_parenteses_1=quant_parenteses_1+1
            if(array_objetos[cont_2][1]==")"):
                quant_parenteses_2=quant_parenteses_2+1
                if(quant_parenteses_1==quant_parenteses_2 and quant_parenteses_1==1):
                    cont_3=cont+2
                    while(cont_3<cont_2):
                        if(array_objetos[cont_3][0]=="KWARG"):
                            key=array_objetos[cont_3][1]
                            arg=array_objetos[cont_3+1][1]
                            kargs_parameters[key]=arg
                            cont_3=cont_3+1
                        elif(array_objetos[cont_3][0]!="SEPARACAO"):
                            arg=array_objetos[cont_3][1]
                            args_parameters.append(arg)
                        cont_3=cont_3+1
                    resultado=tratamento_codigo.funcoes.kwargs_funcoes[funcao_name](*args_parameters,**kargs_parameters)
                    [array_objetos.pop(cont) for valor in range(cont, cont_3 + 1)]
                    if(isinstance(resultado,int) and (resultado!=0 or resultado!=1)):
                        return resultado
                    elif(isinstance(resultado,str)):
                        if("Erro" in resultado):
                            return resultado
                    elif(isinstance(resultado,list)):
                        array_objetos.insert(cont, resultado)
                    elif(resultado==None):
                        return "Erro, ao execultar a função:"+funcao_name
            cont_2=cont_2+1

        return array_objetos
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return str(e)


def run_operacoes(array_objetos, tipo_operacao):
    try:
        cont_obj=1
        while (cont_obj < len(array_objetos)-1):
            if (array_objetos[cont_obj-1][0] == "VALOR" and array_objetos[cont_obj][1] == tipo_operacao and
                        array_objetos[cont_obj + 1][0] == "VALOR"):
                resultado = tratamento_codigo.funcoes.operacao_aritmetica(array_objetos[cont_obj-1][1], tipo_operacao,
                                                        array_objetos[cont_obj + 1][1])

                array_objetos.pop(cont_obj+1)
                array_objetos.pop(cont_obj)
                if(isinstance(resultado,str)):
                    return resultado
                else:
                    array_objetos[cont_obj-1] = ["VALOR", resultado]
                break
            cont_obj = cont_obj + 1
        return array_objetos

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(str(e))


def decode_code(string):
    try:
        variavel = None
        array_objetos = []
        codigo_tratado = tratamento_codigo.pre_tratamento_codigo(string)
        cont=0
        for char in codigo_tratado:
            if(char=="(" or char==")"):
                break
            elif(char=="="):
                variavel=codigo_tratado[:cont]
                codigo_tratado=codigo_tratado[cont+1:]
            cont=cont+1

        if (len(codigo_tratado) != 0):
            array_objetos = tratamento_codigo.sintaxe_analise(codigo_tratado,array_objetos)
        else:
            return "Nenhum texto digitado"
        if(isinstance(array_objetos,list)):
            array_objetos=tratamento_codigo.tratar_objetos(array_objetos)
        else:
            return array_objetos
        if(isinstance(array_objetos,list)):
            print(array_objetos)
            resultado=run_code(array_objetos)
            if(variavel==None):
                variavel="resultado"
            tratamento_codigo.dirt_variaveis[variavel]=resultado[0]
        else:
            return array_objetos
        return resultado
    except Exception as e:
        return 0





