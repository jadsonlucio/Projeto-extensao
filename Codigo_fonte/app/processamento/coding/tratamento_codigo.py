from .simbolos import SIMBOLOS_ARITIMETICOS,SIMBOLOS_CONTENCAO,SIMBOLOS_SERIES_TEMPORAIS,\
                       SIMBOLOS_NUMERICOS,SIMBOLOS_FUNCOES,SIMBOLOS_SEPARACAO,SIMBOLOS_STRINGS

def buscar_simbolo_aritmetico(string,cont,array_objetos):
    try:
        soma_cont=0
        for char_aritimetico in SIMBOLOS_ARITIMETICOS:
            if (string[cont] == char_aritimetico):
                array_objetos.append(["ARITMETICO",char_aritimetico])
                soma_cont=soma_cont+1
        cont=cont+soma_cont
        return cont,array_objetos
    except Exception as e:
        print("buscar_simbolo_aritmetico")

def buscar_simbolo_string(string,cont,array_objetos):
    try:
        soma_cont=0
        for char_serie_key, char_serie_value in zip(SIMBOLOS_STRINGS.keys(), SIMBOLOS_STRINGS.values()):
            if (string[cont] == char_serie_key):
                for cont2 in range(cont+1, len(string)):
                    if (string[cont2] == char_serie_value):
                        array_objetos.append(["STRING",string[cont:cont2+1]])
                        soma_cont=soma_cont+(cont2-cont+1)
                        break;
        cont=cont+soma_cont
        return cont,array_objetos
    except Exception as e:
        print("buscar_simbolo_string")

def buscar_simbolo_contencao(string,cont,array_objetos):
    try:
        soma_cont = 0
        for char_contencao in SIMBOLOS_CONTENCAO:
            if (string[cont] == char_contencao):
                array_objetos.append(["CONTENCAO",char_contencao])
                soma_cont=soma_cont+1
        cont=cont+soma_cont
        return cont,array_objetos
    except Exception as e:
        print("buscar_simbolo_contencao")

def buscar_simbolos_series(string,cont,array_objetos):
    try:
        soma_cont=0
        for char_serie_key, char_serie_value in zip(SIMBOLOS_SERIES_TEMPORAIS.keys(), SIMBOLOS_SERIES_TEMPORAIS.values()):
            if (string[cont] == char_serie_key):

                for cont2 in range(cont+1, len(string)):
                    if (string[cont2] == char_serie_value):
                        array_objetos.append(["VALOR",string[cont:cont2+1]])
                        soma_cont=soma_cont+(cont2-cont+1)
                        break;
        cont=cont+soma_cont
        return cont,array_objetos
    except Exception as e:
        print("buscar_simbolos_series")


def buscar_simbolos_numericos(string,cont,array_objetos):
    try:
        soma_cont=0
        for cont2 in range(cont,len(string)):
            achou_numero=False
            for char_numero in SIMBOLOS_NUMERICOS:
                if(string[cont2]==char_numero):
                    achou_numero=True
                    soma_cont=soma_cont+1
            if(not achou_numero):
                break;
        if(soma_cont>0):
            array_objetos.append(["VALOR",float(string[cont:cont+soma_cont])])
        cont=cont+soma_cont
        return cont,array_objetos
    except Exception as e:
        print("buscar_simbolos_numericos")

def buscar_nomes_funcoes(string,cont,array_objetos):
    try:
        for nome_func in SIMBOLOS_FUNCOES:
            if(nome_func==string[cont:cont+len(nome_func)]):
                array_objetos.append(["FUNCAO",nome_func])
                cont=cont+len(nome_func)
        return cont,array_objetos
    except Exception as e:
        print("buscar_nomes_funcoes")

def buscar_simbolos_separacao(string,cont,array_objetos):
    try:
        soma_cont=0
        for simbolo in SIMBOLOS_SEPARACAO:
            if(string[cont]==simbolo):
                array_objetos.append(["SEPARACAO",simbolo])
                soma_cont=soma_cont+1
                break;
        cont=cont+soma_cont
        return cont,array_objetos
    except Exception as e:
        print("buscar_simbolos_separacao")


