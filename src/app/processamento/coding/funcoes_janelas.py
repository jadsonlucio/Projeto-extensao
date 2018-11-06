from .help.help import load_help_functions
from ...libs import estatisticas
from ...processamento.series_temporais import processamento

def criar_janela_tabela(titulo="",largura=300,altura=300,maximize=True,top_level=True,frames=None):
    from ...backend.tkinter_backend.janelas.janela_tabela import janela_tabela

    janela=janela_tabela.janela_tabela(frames,top_level,False)
    janela.geometry(str(largura)+"x"+str(altura))
    janela.title(titulo)
    if(maximize):
        janela.maximize()
    janela.iniciar_componentes()
    return janela

def criar_janela_help(titulo="",largura=300,altura=300,top_level=None,frames=None):
    try:
        from ...backend.tkinter_backend.janelas.janela_help import janela_help

        help_functions=load_help_functions()
        janela=janela_help.janela_help(help_functions,top_level,frames)
        janela.geometry(str(largura)+"x"+str(altura))
        janela.title(titulo)

        return 0
    except Exception as e:
        return str(e)

def criar_tabela_series(series,formato_data="%d/%m/%Y %H:%M",**tabela_kwargs):
    try:
        array_valores=[]
        if(isinstance(series,processamento.serie_temporal)):
            data_array = series.get_date_serie(format_date=formato_data)
            valor_array = series.ploted_data_y
            data_array.insert(0, "Data")
            valor_array.insert(0, series.text_legenda)
            array_valores.append(data_array)
            array_valores.append(valor_array)
        else:
            for serie in series:
                if(isinstance(serie[1],processamento.serie_temporal)):
                    data_array=serie[1].get_date_serie(format_date=formato_data)
                    valor_array=serie[1].ploted_data_y
                    data_array.insert(0,"Data")
                    valor_array.insert(0,serie[1].text_legenda)
                    array_valores.append(data_array)
                    array_valores.append(valor_array)
                else:
                    return "Erro:Objeto:"+str(serie[1])+", não é do tipo série temporal"

        array_final=estatisticas.criar_matriz_array(array_valores)

        janela = criar_janela_tabela(**tabela_kwargs)
        janela.frame_janela_tabela.tabela.criar_tabela("tabela")
        janela.frame_janela_tabela.set_tabela_data(0,array_final)
        janela.frame_janela_tabela.iniciar_componentes()
        return 0
    except Exception as e:
        return "Erro:"+str(e)