import tkinter as tk
from tkinter import ttk
from ..frame import frame
class frame_janela_help(frame):
    def __init__(self,janela,container,dirc_functions):
        frame.__init__(self,janela,"frame_janela_help",container)
        self.dirc_functions=dirc_functions
        self.array_text=[]

    def load_functions(self,_key=None):
        self.clear_text()
        for key in self.dirc_functions.keys():
            if(_key==None):
                self.add_text(key,self.func_click,self.func_click)
            elif(_key in key):
                self.add_text(key, self.func_click, self.func_click)

    def change_cursor_enter(self, event):
        self.text.config(cursor='hand2')

    def change_cursor_leave(self, event):
        self.text.config(cursor='arrow')

    def add_text(self, text, func_click_left, func_click_right):
        self.array_text.append(text)
        index = len(self.array_text) - 1
        self.text.configure(state='normal')
        self.text.insert('end', text + "\n", text)
        self.text.configure(state='disabled')
        self.text.tag_configure(text, foreground="blue", underline=True)
        self.text.tag_bind(text, "<Button-1>", func_click_left)
        self.text.tag_bind(text, "<Button-2>", func_click_right)
        self.text.tag_bind(text, "<Leave>", self.change_cursor_leave)
        self.text.tag_bind(text, "<Enter>", self.change_cursor_enter)

    def add_normal_text(self,text):
        self.text.configure(state='normal')
        self.text.insert(tk.INSERT, text)
        self.text.configure(state='disabled')

    def clear_text(self):
        self.array_text = []
        self.text.configure(state="normal")
        self.text.delete(1.0, "end")
        self.text.configure(state='disabled')

    def iniciar_componentes(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.pesquisa_text=tk.Entry(self)
        self.pesquisa_text.pack(anchor=tk.NE)
        self.pesquisa_text.bind("<Key>",self.pesquisa_key_event)

        self.xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.xscrollbar.pack(side=tk.BOTTOM,fill=tk.X)

        self.yscrollbar = tk.Scrollbar(self)
        self.yscrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        self.text = tk.Text(self, wrap=tk.NONE, bd=0,
                    xscrollcommand=self.xscrollbar.set,
                    yscrollcommand=self.yscrollbar.set)

        self.text.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)

        self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        for key in self.dirc_functions.keys():
            self.add_text(key,self.func_click,self.func_click)

    def pesquisa_key_event(self,event):
        text_pesquisa=self.pesquisa_text.get()
        self.load_functions(text_pesquisa)

    def func_click(self,event):
        key = event.widget.tag_names(tk.CURRENT)[0]
        self.clear_text()
        file_text=self.dirc_functions[key]
        file_text.seek(0)
        self.add_normal_text(file_text.read())