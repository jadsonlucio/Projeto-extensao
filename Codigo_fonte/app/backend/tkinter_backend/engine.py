import tkinter as tk
from . import objetos
from . import tktable
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Toplevel
from tkinter import Frame


class eventos():
    def __init__(self, widget):
        self.widget = widget
        self.iniciar_eventos()

    def iniciar_eventos(self):
        try:
            self.widget.bind('<Enter>', self.enter_event)
            self.widget.bind('<Leave>', self.leave_event)
            self.widget.bind('<Key>', self.key_press)
            self.widget.bind('<Button-1>', self.click_event)
            self.widget.bind('<B1-Motion>', self.motion_event)
            self.widget.bind('<ButtonRelease-1>', self.release_event)
            self.widget.bind('<Configure>', self.config_event)
            self.widget.bind('<FocusIn>',self.focusin_event)
            self.events_keys=["Enter","Leave","Key","Button-1","B1-Motion","ButtonRelease-1","Configure","FocusIn"]
            self.events={}
            self.events_info={}
            for event_key in self.events_keys:
                self.events[event_key]=[]
        except Exception as e:
            pass

    def add_event(self,func,tipo_evento):
        try:
            for _tipo_evento in self.events_keys:
                if(tipo_evento==_tipo_evento):
                    self.events[tipo_evento].append(func)
            raise ValueError("Tipo de evento não encontrado")
        except Exception as e:
            pass
    #funcões eventos widget

    def enter_event(self, event):
        self.events_info["widget"]=event.widget
        for event in self.events["Enter"]:
            event(self.events_info)

    def leave_event(self, event):
        self.events_info["widget"] = event.widget
        for event in self.events["Leave"]:
            event(self.events_info)

    def key_press(self, event):
        self.events_info["key_press"]=event.char
        self.events_info["key_code"]=event.keycode
        for event in self.events["Key"]:
            event(self.events_info)

    def click_event(self, event):
        self.events_info["widget"] = event.widget
        self.events_info["x"]=event.x
        self.events_info["y"]=event.y
        for event in self.events["Button-1"]:
            event(self.events_info)

    def motion_event(self, event):
        self.events_info["widget"] = event.widget
        self.events_info["x"]=event.x
        self.events_info["y"]=event.y
        for event in self.events["B1-Motion"]:
            event(self.events_info)


    def release_event(self, event):
        self.events_info["x"]=event.x
        self.events_info["y"]=event.y
        for event in self.events["ButtonRelease-1"]:
            event(self.events_info)


    def config_event(self, event):
        self.events_info["width"]=event.width
        self.events_info["height"]=event.height
        for event in self.events["Configure"]:
            event(self.events_info)

    def focusin_event(self,event):
        pass

