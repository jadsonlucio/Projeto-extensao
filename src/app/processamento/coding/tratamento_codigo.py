from .simbolos import SIMBOLOS_ARITIMETICOS,SIMBOLOS_CONTENCAO,SIMBOLOS_SERIES_TEMPORAIS,\
                       SIMBOLOS_NUMERICOS,SIMBOLOS_SEPARACAO,SIMBOLOS_STRINGS


from . import funcoes

SIMBOLOS_FUNCOES=funcoes.kwargs_funcoes.keys()
kargs_type=["VALOR","ARRAY","STRING"]
valor_type=["ARITMETICO","SEPARACAO"]

dirt_variaveis={"PI":['VALOR',3.14],"e":['VALOR',2.718]}
substituicoes_padrao=[[' ',''],['\n','']]

def pre_tratamento_codigo(string,array_substituicoes=substituicoes_padrao,decode="utf-8"):
    try:
        new_string=""
        for char in string:
            if(char!="\n"):
                new_string=new_string+char
        return new_string
    except Exception as e:
        return 0

def sintaxe_analise(string,array_objetos,array_funcoes_procura=None):
    try:
        if(array_funcoes_procura==None):
            array_funcoes_procura = [buscar_simbolo_aritmetico, buscar_simbolo_contencao,
                                     buscar_simbolos_series, buscar_simbolos_numericos,
                                     buscar_nomes_funcoes, buscar_variaveis,buscar_simbolo_string]

        achou_erro = False
        cont = 0
        while (cont < len(string)):
            valor_erro = len(array_objetos)
            for func_procura in array_funcoes_procura:
                resultado = func_procura(string, cont, array_objetos)
                if(not isinstance(resultado,tuple)):
                    return resultado
                else:
                    cont, array_objetos=resultado
                if (cont >= len(string)):
                    break
            if (len(array_objetos) == valor_erro):
                achou_erro = True
                break

        if (achou_erro):
            return cont
        else:
            return array_objetos
    except Exception as e:
        return 0

def semantica_analise(array_objetos):
    try:
        cont = 0
        cont_1 = 0
        cont_2 = 0
        for obj in array_objetos:
            if (isinstance(obj[1], str)):
                if (obj[1] == "("):
                    cont_1 = cont_1 + 1
                if (obj[1] == ")"):
                    cont_2 = cont_2 + 1
        if (cont_1 != cont_2):
            return "Numero parênteses incorreto"

        for cont_obj in range(0, len(array_objetos)-1):
            encontrou_compativel=False
            if(array_objetos[cont_obj][0]=="KWARG"):
                for type in kargs_type:
                    if(array_objetos[cont_obj+1][0]==type):
                        encontrou_compativel=True
            elif(array_objetos[cont_obj][0]=="VALOR"):
                pass

            if(not encontrou_compativel):
                return "Erro,"+str(array_objetos[cont_obj][1])+","+str(array_objetos[cont_obj+1][1])

        return array_objetos
    except Exception as e:
        print("semantica_analise")


def tratar_objetos(array_objetos):
    try:
        new_array_objetos = []
        for cont_objetos in range(0, len(array_objetos)):
            if (array_objetos[cont_objetos][0] == "ARRAY"):
                resultado=[]
                tratar_array(array_objetos[cont_objetos][1],resultado)
                if(len(resultado)==1):
                    new_array_objetos.append(resultado[0])
                else:
                    new_array_objetos.append(["ARRAY",resultado])
            else:
                new_array_objetos.append(array_objetos[cont_objetos])
        cont_objetos=0
        while(cont_objetos<len(new_array_objetos)-1):
            if(new_array_objetos[cont_objetos][0]=="ARRAY" and new_array_objetos[cont_objetos+1][0]=="VALOR"):
                try:
                    index=int(new_array_objetos[cont_objetos+1][1][0])
                    if(index>len(new_array_objetos[cont_objetos][1])-1):
                        return "Erro index "+str(new_array_objetos[cont_objetos+1][1])+",valor muito alto"
                    else:
                        new_array_objetos[cont_objetos]=new_array_objetos[cont_objetos][1][index]
                        new_array_objetos.remove(new_array_objetos[cont_objetos+1])
                        cont_objetos=cont_objetos-1
                except Exception as e:
                    return "Erro "+str(new_array_objetos[cont_objetos+1][1])+" não é inteiro"

            cont_objetos=cont_objetos+1

        return new_array_objetos


    except Exception as e:
        return 0


def tratar_array(array, novo_array):
    try:
        for obj in array:
            if (obj[0] == "ARRAY"):
                _novo_array = []
                novo_array.append(_novo_array)
                tratar_array(obj[1], _novo_array)
            elif (obj[0] == "STRING"):
                objeto = tratar_array_text(obj[1])
                if(objeto!=None):
                    novo_array.append(objeto)
            else:
                novo_array.append(obj)
    except Exception as e:
        return 0


def tratar_array_text(string):
    if (string == ""):
        return None
    elif ("->" in string):
        return ["VALOR",funcoes.criar_serie_temporal(string)]
    elif (":" in string):
        return ["VALOR",funcoes.pegar_serie_temporal(string)]
    else:
        return ["STRING",string]

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
        for char_serie_key, char_serie_value in zip(SIMBOLOS_STRINGS.keys(), SIMBOLOS_STRINGS.values()):
            if (string[cont] == char_serie_key):
                for cont2 in range(cont+1, len(string)):
                    if (string[cont2] == char_serie_value):
                        array_objetos.append(["STRING",string[cont+1:cont2]])
                        cont=cont2+1
                        break;

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
    if(string[cont]=="["):
        quant_cochetes_1=0
        quant_cochetes_2=0
        for cont_aux in range(cont,len(string)):
            if(string[cont_aux]=="["):
                quant_cochetes_1=quant_cochetes_1+1
            elif(string[cont_aux]=="]"):
                quant_cochetes_2 = quant_cochetes_2 + 1
                if(quant_cochetes_1==quant_cochetes_2):
                    array_objetos.append(split_array(string[cont:cont_aux+1],',')[0])
                    cont=cont_aux+1
                    break
    return cont,array_objetos

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
                break
        if(soma_cont>0):
            array_objetos.append(["VALOR",float(string[cont:cont+soma_cont])])

        return cont+soma_cont,array_objetos
    except Exception as e:
        print("buscar_simbolos_numericos")

def buscar_variaveis(string, cont, array_objetos):
    try:
        soma_cont = 0
        for key in dirt_variaveis.keys():
            if (string[cont:cont+len(key)] == key):
                array_objetos.append(dirt_variaveis[key])
                soma_cont = soma_cont + len(key)
                break
        cont = cont + soma_cont
        return cont, array_objetos
    except Exception as e:
        print("buscar_variaveis")

def buscar_nomes_funcoes(string,cont,array_objetos):
    try:

        array_funcoes_procura = [buscar_simbolo_aritmetico, buscar_simbolo_contencao,
                                 buscar_simbolos_series, buscar_simbolos_numericos,
                                 buscar_nomes_funcoes, buscar_variaveis,buscar_simbolo_string,
                                 buscar_simbolos_separacao,buscar_simbolos_kwargs]
        for nome_func in SIMBOLOS_FUNCOES:
            cont_len_func=cont+len(nome_func)
            if(nome_func==string[cont:cont_len_func]):
                array_objetos.append(["FUNCAO",nome_func])
                if(string[cont_len_func]=="("):
                    quant_parenteses_1=0
                    quant_parenteses_2=0
                    for cont_char in range(cont_len_func,len(string)):
                        if(string[cont_char]=="("):
                            quant_parenteses_1=quant_parenteses_1+1
                        elif(string[cont_char]==")"):
                            quant_parenteses_2=quant_parenteses_2+1
                            if(quant_parenteses_1==quant_parenteses_2):
                                cont=cont_char+1
                                array_objetos=sintaxe_analise(string[cont_len_func:cont_char+1],array_objetos,array_funcoes_procura)
                                if(not isinstance(array_objetos,list)):
                                    return array_objetos
                                break
                        if(cont_char==len(string)-1 and (quant_parenteses_1!=quant_parenteses_2)):
                            return "Erro,quantidade de parenteses incorreta na função:"+nome_func
                else:
                    return "Erro,falta de parenteses na funcão:"+nome_func
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

def buscar_simbolos_kwargs(string,cont,array_objetos):
    try:
        for cont_string in range(cont,len(string)):
            if(string[cont_string]==","):
                break
            if(string[cont_string]=="="):
                array_objetos.append(["KWARG",string[cont:cont_string]])
                cont=cont_string+1
                break
        return cont,array_objetos
    except Exception as e:
        print(str(e))

def split_array(string,char_split):
    array_resultado=[]
    cont_string=0
    while(cont_string<len(string)):
        if(cont_string==0):
            valor_inicial=cont_string
        if(cont_string==len(string)-1):
            try:
                valor_double=float(string[valor_inicial:cont_string+1])
                array_resultado.append(["VALOR",valor_double])
            except:
                array_resultado.append(["STRING",string[valor_inicial:cont_string+1]])
        elif(string[cont_string]=="[" and valor_inicial==cont_string):
            valor_inicial=cont_string
            quant_cochetes_1=0
            quant_cochetes_2=0
            while(cont_string<len(string)):
                if(string[cont_string]=="["):
                    quant_cochetes_1=quant_cochetes_1+1
                elif(string[cont_string]=="]"):
                    quant_cochetes_2=quant_cochetes_2+1
                    if(quant_cochetes_1==quant_cochetes_2):
                        if(cont_string==len(string)-1):
                            result=split_array(string[valor_inicial + 1:cont_string], ',')
                            achou_array_string=False
                            for array in result:
                                if(array[0]=="STRING" or quant_cochetes_1>1):
                                    achou_array_string=True
                            if(achou_array_string==False):
                                array_resultado.append(["VALOR",[array[1] for array in result]])
                            else:
                                array_resultado.append(["ARRAY",result])
                            break
                        elif(string[cont_string+1]==char_split):
                            result=split_array(string[valor_inicial + 1:cont_string], ',')
                            achou_array_string=False
                            for array in result:
                                if(array[0]=="STRING" or quant_cochetes_1>1):
                                    achou_array_string=True
                            if(achou_array_string==False):
                                array_resultado.append(["VALOR",[array[1] for array in result]])
                            else:
                                array_resultado.append(["ARRAY",result])
                            cont_string=cont_string+1
                            valor_inicial=cont_string+1
                            break
                        else:
                            return -1
                cont_string=cont_string+1
        elif(string[cont_string]==","):
            try:
                valor_double=float(string[valor_inicial:cont_string])
                array_resultado.append(["VALOR",valor_double])
            except:
                array_resultado.append(["STRING",string[valor_inicial:cont_string]])
            valor_inicial=cont_string+1

        cont_string=cont_string+1
    return array_resultado
