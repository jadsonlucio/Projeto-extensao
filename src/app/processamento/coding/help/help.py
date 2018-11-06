from ...arquivo import list_files,abrir_arquivo,split_url
from ...exceptions.exception import tratamento_excessao,infoerroexception
from ....constantes import CAMINHO_HELP_FUNCTIONS_FILES

def load_help_functions():
    try:
        dirt_functions={}
        files=list_files(CAMINHO_HELP_FUNCTIONS_FILES)

        for file_name in files:
            dirt_functions[split_url(file_name)["file_name"]]=abrir_arquivo(CAMINHO_HELP_FUNCTIONS_FILES+"//"+file_name)

        return dirt_functions
    except Exception as e:
        tratamento_excessao("Erro")