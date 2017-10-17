from calendar import monthrange
from datetime import date
from os import path
from dateutil.relativedelta import relativedelta

from ..constantes import CAMINHO_BACKUP
from ..processamento.arquivo import copiar_arquivo
from .exceptions.exception import infoerroexception,tratamento_excessao

data_inicial = [2013, 1]
abreviacao_datas = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

#funcão organizar arquivo por datas

def organizar_arquivos(files_url):
    try:
        files_names = [path.split(file_url)[1] for file_url in files_url]
        files_url = list(files_url)
        arquivos_organizados = []
        for ano in range(2012, 2030):
            for cont_mes in range(0, 12):
                for file_name, file_url in zip(files_names, files_url):
                    file_name_lower = str(file_name).lower()
                    if (abreviacao_datas[cont_mes] in file_name_lower and str(ano) in file_name_lower):
                        arquivos_organizados.append([file_name, file_url, ano, cont_mes + 1])
                        copiar_arquivo(file_url, CAMINHO_BACKUP)
                        files_names.remove(file_name)
                        files_url.remove(file_url)
        if (files_names):
            raise FileExistsError("Os seguintes arquivos não possuem os requisitos de "
                                  "nomenclatura para serem adicionados:\n" + "\n".join(files_names))
    except Exception as e:
        tratamento_excessao(type_exception='Erro')

    return arquivos_organizados

#funções operações com datas

def operacao_datas(operador='+', data_ini=date, data_fim=date):
    try:
        if (data_fim.year < data_ini.year):
            raise ValueError("Data final menor que data inicial")
        elif (data_fim.year == data_ini.year and data_fim.month < data_ini.month):
            raise ValueError("Data final menor que data inicial")
        elif (data_ini.month == data_fim.month and data_fim.day < data_fim.day):
            raise ValueError("Data final menor que data inicial")
        if (operador == '+'):
            data_final = data_fim + data_ini
        if (operador == '-'):
            data_final = data_fim - data_ini
        return data_final.days
    except ValueError as e:
        tratamento_excessao("Info")
    except Exception as e:
        tratamento_excessao(type_exception='Erro')

def month_range(mes=1, ano=2013):
    resultado = monthrange(year=ano, month=mes)
    return resultado

def somar_periodos(periodo, time_steps, data):
    try:
        data_fim=None
        if (periodo == 'segundos'):
            data_fim = data + relativedelta(seconds=time_steps)
        if (periodo == 'minutes' or periodo == 'minuto'):
            data_fim = data + relativedelta(minutes=time_steps)
        if (periodo == 'horas'):
            data_fim = data + relativedelta(hours=time_steps)
        if (periodo == 'dias'):
            data_fim = data + relativedelta(days=time_steps)
        if (periodo == 'meses'):
            data_fim = data + relativedelta(months=time_steps)
        if (periodo == 'anos'):
            data_fim = data + relativedelta(years=time_steps)

        return data_fim
    except Exception as e:
        tratamento_excessao(type_exception='Erro')


def converter_periodo(periodo, periodo_convertido):
    if (periodo == 'minuto'):
        if (periodo_convertido == 'dia'):
            return 1 / (24 * 60)
        if (periodo_convertido == 'hora'):
            return 1/60
        if (periodo_convertido == 'minuto'):
            return 1
    if (periodo == 'hora'):
        if (periodo_convertido == 'dia'):
            return 1 / 24
        if (periodo_convertido == 'minuto'):
            return 60
        if (periodo_convertido == 'hora'):
            return 1
    if (periodo == 'dia'):
        if (periodo_convertido == 'hora'):
            return 24
        if (periodo_convertido == 'minuto'):
            return 24*60
        if (periodo_convertido == 'dia'):
            return 1

def converter_string_to_date(string,separador):
    try:
        if(len(string.split(separador))==3):
            dia,mes,ano=[int(valor) for valor in string.split(separador)]
            data=date(day=dia,month=mes,year=ano)
            return data
        else:
            raise infoerroexception("Data invalida")
    except infoerroexception as e:
        tratamento_excessao("Info")
    except Exception as e:
        tratamento_excessao("Erro")

def criar_arraydate(data_inicial, iteracoes, periodo, time_steps,itercoes_ini=0):
    try:
        arraydate = []
        for cont in range(itercoes_ini, iteracoes):
            arraydate.append(somar_periodos(periodo, time_steps * cont, data_inicial))

        return arraydate
    except Exception as e:
        tratamento_excessao(type_exception='Erro')

def criar_array_date(array_x,data_inicial,periodo,time_steps):
    try:
        array_date=[]
        for x_value in array_x:
            array_date.append(somar_periodos(periodo,time_steps*x_value,data_inicial))
        return array_date
    except Exception as e:
        tratamento_excessao("Erro")
