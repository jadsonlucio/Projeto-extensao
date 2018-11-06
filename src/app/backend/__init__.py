_BACKEND='tkinter'
backend_selecionado=None

def _backend():
    return _BACKEND
def backend():
    return backend_selecionado

if(_BACKEND=='tkinter'):
    from . import tkinter_backend
    backend_selecionado= tkinter_backend

elif(_BACKEND=='kivy'):
    from . import kivy_backend
    backend_selecionado = kivy_backend
else:
    raise ValueError('backend ' + str(_BACKEND)+" não suportado")