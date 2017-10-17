import sys
import warnings

from ... import constantes, backend

# Variaveis globais
CAMINHO_FILE_ERROS_APP=constantes.CAMINHO_FILE_ERROS_APP


def tratamento_excessao(type_exception='Erro'):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    ftraceback_details = {
        'filename': exc_tb.tb_frame.f_code.co_filename,
        'lineno': exc_tb.tb_lineno,
        'name': exc_tb.tb_frame.f_code.co_name,
        'type': exc_type.__name__,
        'message': exc_obj,
    }

    if (type_exception == 'Info'):
        if(backend.backend_selecionado!=None):
            backend.backend_selecionado.engine.messagebox.showinfo('Info', ftraceback_details['message'])
        else:
            warnings.showwarning(ftraceback_details['message'],Warning,ftraceback_details['filename'],
                                              ftraceback_details['lineno'],ftraceback_details['name'])
    elif (type_exception == 'Erro'):
        msg = str(ftraceback_details)+"\n"
        erro_logs = open(CAMINHO_FILE_ERROS_APP,"a+")
        erro_logs.writelines(msg)
        result = backend.backend_selecionado.engine.messagebox.askyesno('Erro', 'Um erro inesperado aconteceu\ndeseja continuar utilizando o programa?')
        if (result == 0):
            sys.exit()

class infoerroexception(Exception):
    pass
