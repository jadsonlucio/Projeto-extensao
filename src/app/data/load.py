from tkinter import PhotoImage
from ..processamento.exceptions.exception import tratamento_excessao,infoerroexception

def load_icones():
    try:
        icones = {}
        icones['icon_add'] = PhotoImage(file='data//icones//icones_botoes//add.png')
        icones['icon_create'] = PhotoImage(file='data//icones//icones_botoes//create.png')
        icones['icon_draw'] = PhotoImage(file='data//icones//icones_botoes//desenhar.png')
        return icones
    except Exception as e:
        tratamento_excessao(type_exception='Erro')
