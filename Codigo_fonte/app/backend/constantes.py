from . import _BACKEND

CAMINHO_JANELA_INICIAL=""
CAMINHO_JANELA_SERIES=""
CAMINHO_JANELA_ESTATISTICAS="app//backend//tkinter_backend//janelas//janela_estatisticas//janela_parametros.ini"
CAMINHO_JANELA_PARAMETROS=""
CAMINHO_FRAMES_INI=""
CAMINHO_ICONS_FRAME_INI="app//data//icones//icones_botoes//"
CAMINHO_ICONS_FRAME_SERIES="app//data//icones//icones_botoes//"
CAMINHO_ICONS_FRAME_CODE="app//data//icones//icones_botoes//"
if(_BACKEND=="tkinter"):
    CAMINHO_JANELA_INICIAL="app//backend//tkinter_backend//janelas//janela_inicial//janela_inicial.ini"
    CAMINHO_JANELA_SERIES="app//backend//tkinter_backend//janelas//janela_series_temporais//janela_series_temporais.ini"
    CAMINHO_JANELA_ESTATISTICAS="app//backend//tkinter_backend//janelas//janela_estatisticas//janela_parametros.ini"
    CAMINHO_JANELA_PARAMETROS="app//backend//tkinter_backend//janelas//janela_parametros//janela_parametros.ini"
    CAMINHO_FRAMES_INI="app//backend//tkinter_backend//frames//frames.ini"
elif(_BACKEND=="kivy"):
    CAMINHO_JANELA_INICIAL="app/backend//kivy_backend//janelas//janela_inicial//janela_inicial.ini"
    CAMINHO_JANELA_SERIES="app//backend//kivy_backend//janelas//janela_series_temporais//janela_series_temporais.ini"
    CAMANHO_JANELA_ESTATISTICAS = "app//backend//kivy_backend//janelas//janela_estatisticas//janela_parametros.ini"
    CAMINHO_FRAMES_INI = "app//backend//kivy_backend//frames//frames.ini"