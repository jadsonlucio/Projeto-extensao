import tkinter as tk
from tkinter import ttk

class Table(ttk.Treeview):

    def update_colums(self):
        self["columns"]=tuple(self.columns)
        for cont_column in range(0,len(self.columns)):
            self.heading("#"+str(cont_column+1),text=self.columns[cont_column])
            self.column("#"+str(cont_column+1),anchor=tk.CENTER,stretch=True,minwidth=self.column_min_width)

    def __init__(self,container,columns,rows=[],baground_head_color="ligthgray",background_cel_color="gainsboro",
                 foreground_head_color="black",foreground_cel_color="blue",font_head=("Arial",13),font_cell=("Arial",12),
                 scroll_x=True,scroll_y=True,column_min_width=150):
        self.background_head_color=baground_head_color
        self.background_cel_color=background_cel_color
        self.foreground_head_color=foreground_head_color
        self.foreground_cel_color=foreground_cel_color
        self.font_head=font_head
        self.font_cell=font_cell
        self.column_min_width=column_min_width
        self.columns=[]
        self.rows=[]
        self.itens=[]
        self.container=container
        ttk.Treeview.__init__(self,container,show="headings")

        self["columns"]=tuple(columns)


        if(scroll_x):
            self.scroll_bar_x = ttk.Scrollbar(self.container, orient="horizontal", command=self.xview)
            self.scroll_bar_x.place(height=20,relwidth=1,x=0,rely=1,y=-20)
            self.configure(xscrollcommand=self.scroll_bar_x.set)
        if(scroll_y):
            self.scroll_bar_y = ttk.Scrollbar(self.container, orient="vertical", command=self.yview)
            self.scroll_bar_y.place(relheight=1,width=20,y=0,relx=1,x=-20)
            self.configure(yscrollcommand=self.scroll_bar_y.set)

        if(len(rows)>0 and len(columns)>0):
            for column in columns:
                self.add_column(column)
            for row in rows:
                self.add_row(row)
        elif(len(columns)>0):
            for column in columns:
                self.add_column(column)
        elif(len(rows)>0 and len(columns)==0):
            print("Erro")

        #config style

        style = ttk.Style()
        style.configure("Custom.Treeview.Heading",
                        background=self.background_head_color, foreground=self.foreground_head_color
                        ,font=self.font_head, relief="RIDGE", borderwidth=6,bordercolor="blue")
        style.map("Custom.Treeview.Heading",
                  relief=[('active', 'RIDGE'), ('pressed', 'sunken')])
        style.configure("Custom.Treeview",
                        background=self.background_cel_color, foreground=self.foreground_cel_color,
                        font=self.font_cell, borderwidth=6)

        self.config(style="Custom.Treeview")

    def set_data(self,array_data):
        self.clear_rows()
        for array in array_data:
            self.add_row(array)

    def set_header(self,array):
        self.columns=array
        self.update_colums()

    def cell(self,row,column,value=None):
        if(value==None):
            return self.set(self.itens[row],column)
        else:
            self.set(self.itens[row],column,value)


    def add_column(self,column_name):
        self.columns.append(column_name)
        self.update_colums()

    def remove_column(self,index_column):
        self.columns.remove(self.columns[index_column])
        self.update_colums()

    def add_row(self,array_valores,index="end"):
        self.rows.append(array_valores)
        self.itens.append(self.insert("",index,values=tuple(array_valores)))

    def remove_row(self,index):
        try:
            self.delete(self.itens[index])
        except Exception as e:
            print(str(e))
    def clear_rows(self):
        for cont in range(0,len(self.itens)):
            self.remove_row(cont)
        self.rows.clear()
        self.itens.clear()