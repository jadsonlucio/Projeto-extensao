from os import listdir, remove, rmdir ,path,makedirs
from shutil import copy2, rmtree

from ..backend import backend_selecionado
from .exceptions.exception import tratamento_excessao,infoerroexception


# Operações de arquivos
def criar_arquivo(nome_arquivo,caminho_arquivo):
    if(not verificar_arquivo(caminho_arquivo,nome_arquivo)):
        return open(caminho_arquivo+nome_arquivo,'w')
    else:
        raise infoerroexception("Arquivo que já existe")

def abrir_arquivo(file_url):
    file = open(file_url, 'r+')
    return file

def deletar_arquivo(url, nome_arquivo):
    try:
        if (not nome_arquivo and not list_files(url)):
            rmdir(url)
        if (not nome_arquivo and list_files(url)):
            result = backend_selecionado.box.askyesno('Apagar', 'Deseja apagar todos\nos arquivos dessa pasta?')
            if (result == 1):
                rmtree(url)
        if (nome_arquivo):
            remove(url + nome_arquivo)
    except Exception as e:
        tratamento_excessao(type_exception='Erro')


def copiar_arquivo(url_arquivo, url_destino):
    try:
        copy2(url_arquivo, url_destino)
    except Exception as e:
        tratamento_excessao(type_exception='Erro')


def list_files(url):
    try:
        list_files = listdir(url)
        return list_files
    except Exception as e:
        tratamento_excessao(type_exception='Erro')

def filter_files(files_list,files_ext):
    try:
        resultado=[]
        for file_name in files_list:
            if(isinstance(files_ext,str)):
                if(file_name.endswith(files_ext)):
                    resultado.append(file_name)
            else:
                for file_ext in files_ext:
                    if (file_name.endswith(file_ext)):
                        resultado.append(file_name)
                        break
        return resultado
    except Exception as e:
        tratamento_excessao("Erro")

def verificar_arquivo(caminho_arquivo, nome_arquivo):
    try:
        files_names = list_files(caminho_arquivo)
        for file_name in files_names:
            if (file_name == nome_arquivo):
                return True
        return False
    except Exception as e:
        tratamento_excessao(type_exception='Erro')


# Operações de arquivos

def ler_array_arquivo(arquivo):
    try:
        array=[]
        for linha in arquivo.readlines():
            array.append(linha.replace('\n', '').replace('\r', ''))
        arquivo.close()
        return array
    except Exception as e:
        tratamento_excessao(type_exception='Erro')


def salvar_array_arquivo(arquivo,data_array):
    try:
        if(isinstance(data_array,str)):
            arquivo.write(data_array.replace('[', '').replace(']', '') + '\n')
        else:
            for linha in data_array:
                arquivo.write(str(linha).replace('[', '').replace(']', '') + '\n')
        arquivo.close()
    except Exception as e:
        tratamento_excessao(type_exception='Erro')


def converter_array_to_dictonary(array):
    try:
        dicionario = {}
        for line in array:
            key, arg = str(line).split('=')
            dicionario[str(key)] = str(arg)
        return dicionario
    except Exception as e:
        tratamento_excessao(type_exception='Erro')

def converter_dictonary_to_array(dirt):
    try:
        array=[]
        for key,value in zip(dirt.keys(),dirt.values()):
            array.append(str(key)+"="+str(value))
        return array
    except Exception as e:
        tratamento_excessao("Erro")

def join_dirt(dirt_1,dirt_2):
    try:
        for key,value in zip(dirt_2.keys(),dirt_2.values()):
            dirt_1[key]=value
        return dirt_1
    except Exception as e:
        tratamento_excessao("Erro")

# leitura personalizada

def ler_arquivo_metricas(url_arquivo):
    return converter_array_to_dictonary(ler_array_arquivo(abrir_arquivo(url_arquivo)))

#operações com diretorios

def split_url(url_arquivo):
    try:
        dirt_resultado={
            "url_file":path.dirname(url_arquivo)+"//",
            "file_name":path.splitext(path.basename(url_arquivo))[0],
            "file_extension":path.splitext(path.basename(url_arquivo))[1]
        }
        return dirt_resultado
    except Exception as e:
        tratamento_excessao("Erro")

def create_dir(url_dir):
    try:
        if(not path.exists(url_dir)):
            makedirs(url_dir)
        else:
            raise infoerroexception("Diretorio já existe")
    except infoerroexception as e:
        tratamento_excessao("Info")
    except Exception as e:
        tratamento_excessao("Erro")