import os

from . import backend
from . import instancias
from . import libs
from . import processamento

from .constantes import CAMINHO_INFORMACOES_APP

__versao__="0.1"
__informacoes__=""

if(os.path.exists(CAMINHO_INFORMACOES_APP)):
    arquivo= processamento.arquivo.abrir_arquivo(CAMINHO_INFORMACOES_APP)
    __informacoes__=processamento.arquivo.converter_array_to_dictonary(
        processamento.arquivo.ler_array_arquivo(arquivo))
else:
    raise ValueError("O caminho "+CAMINHO_INFORMACOES_APP+" não existe")