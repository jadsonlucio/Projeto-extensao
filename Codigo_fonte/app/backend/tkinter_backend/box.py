
from .engine import filedialog
from .engine import messagebox

def show_info(titulo,mensagem):
    messagebox.showinfo(titulo,mensagem)

def show_warning(titulo,mensagem):
    messagebox.showwarning(titulo,mensagem)

def show_error(titulo,mensagem):
    messagebox.showerror(titulo,mensagem)

def askyesno(titulo,mensagem):
    valor=messagebox.askyesno(titulo,mensagem)
    return valor

def openfiles(filetypes):
    try:
        files_choice = filedialog.askopenfilenames(filetypes=filetypes)
        return files_choice
    except Exception as e:
        print(str(e))

def opendirectory():
    try:
        url_directory = filedialog.askdirectory()
        return url_directory
    except Exception as e:
        pass