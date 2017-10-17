import tkinter as tk
from os.path import splitext
from ...processamento.arquivo import list_files,filter_files

def load_icons(url_icons,files_ext):
    try:
        dirt={}
        files=filter_files(list_files(url_icons),files_ext)
        for file in files:
            img_load=tk.PhotoImage(file=url_icons+file)
            dirt[splitext(file)[0]]=img_load
        return dirt
    except Exception as e:
        print(str(e))