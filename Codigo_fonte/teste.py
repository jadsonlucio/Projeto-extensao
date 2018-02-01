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

teste="[1,3,3,4]"
print(len(teste))
resultado=split_array(teste,',')
print(resultado)