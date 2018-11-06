import tkinter as tk
from os.path import splitext
from ...processamento.arquivo import list_files,filter_files

dict_files=None

def load_icons(url_icons,files_ext,reload=False):
    global dict_files
    try:
        if(dict_files==None or reload==True):
            dict_files={}
            files=filter_files(list_files(url_icons),files_ext)
            for file in files:
                img_load=tk.PhotoImage(file=url_icons+file)
                dict_files[splitext(file)[0]]=img_load

        return dict_files

    except Exception as e:
        print(str(e))