import os

from . import backend
from . import instancias
from . import libs
from . import processamento

from .constantes import CAMINHO_INFORMACOES_APP

__versao__="0.1"
__PathApp__=__path__[0]

print(__path__)
print(os.listdir(__path__[0]))


arquivo= processamento.arquivo.abrir_arquivo(__PathApp__+"/"+CAMINHO_INFORMACOES_APP)
__informacoes__=processamento.arquivo.converter_array_to_dictonary(
processamento.arquivo.ler_array_arquivo(arquivo))
