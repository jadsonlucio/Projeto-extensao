import tkinter as tk
from ..engine import eventos,Toplevel
from ....processamento import arquivo

class janela(tk.Tk):

    #gets e sets

    def get_frame(self,key_frame):
        try:
            for key in self.frames.keys():
                if(key==key_frame):
                    return self.frames[key_frame]
            raise ValueError("Nome não foi encontrado")
        except Exception as e:
            pass

    def get_size(self):
        try:
            return {"width":self.winfo_width(),"height":self.winfo_height()}
        except Exception as e:
            pass

    def get_position(self):
        try:
            return {"x": self.winfo_x(), "y": self.winfo_y()}
        except Exception as e:
            pass

    def get_mouse_position(self):
        try:
            return {"x": self.winfo_pointerx(),"y": self.winfo_pointery()}
        except Exception as e:
            pass

    def __init__(self,top_level,frames):
        if(top_level==None):
            tk.Tk.__init__(self)
        else:
            Toplevel.__init__(self,master=top_level)
        self.eventos=eventos(self)
        self.top_level=top_level
        self.frames_padrao=frames
        self.frames={}

    def iniciar_componentes(self,frames=None,frames_keys=None):
        try:
            self.container = tk.Frame(self)
            self.container.grid_rowconfigure(0, weight=1)
            self.container.grid_columnconfigure(0, weight=1)
            self.container.pack(fill='both', expand=1)

        except Exception as e:
            print(str(e))

    def show_frame(self,key_frame):
        try:
            self.current_frame=self.get_frame(key_frame)
            self.current_frame.tkraise()
        except Exception as e:
            print(str(e))

    def add_frames(self,frames=None,key_values=None):
        try:
            if(key_values!=None and len(frames)==len(key_values)):
                for frame,key_value in zip(frames,key_values):
                    self.frames[key_value]=frame
                    self.frames[key_value].grid(row=0,column=0,sticky=tk.NSEW)
            elif(frames!=None and key_values==None):
                for frame in frames:
                    self.frames[frame.key] = frame
                    self.frames[frame.key].grid(row=0, column=0, sticky=tk.NSEW)
            else:
                raise ValueError("Nenhum frame encontrado para adicionar")
        except Exception as e:
            print(str(e))

    #Funcões de configuração da janela
    def set_config(self,url_config):
        try:
            dirt=arquivo.converter_array_to_dictonary(arquivo.ler_array_arquivo(arquivo.abrir_arquivo(url_config)))
            self.geometria="800x600+0+0"
            self.titulo="*"
            for key in dirt.keys():
                if(key=="titulo"):
                    self.titulo=dirt[key]
                if(self.top_level==None and key=="geometry"):
                    self.geometria=dirt[key]
                elif(self.top_level!=None and key=="geometry"):
                    config_geometria=[float(valor) for valor in dirt["geometry"].split(",")]
                    top_level_size=self.top_level.get_size()
                    top_level_position=self.top_level.get_position()
                    if(config_geometria[0]==0 and config_geometria[1]==0):
                        x=top_level_position["x"]+top_level_size["width"]*config_geometria[2]
                        y=top_level_position["y"]+top_level_size["height"]*config_geometria[3]
                        self.geometria = "+"+str(int(x))+"+"+str(int(y))
                    elif(config_geometria[0]<=1 and config_geometria[1]<=1):
                        width=top_level_size["width"]*config_geometria[0]
                        height=top_level_size["heigth"]*config_geometria[1]
                        x=top_level_position["x"]+top_level_size["width"]*config_geometria[2]
                        y=top_level_position["y"]+top_level_size["height"]*config_geometria[3]
                        self.geometria=str(width)+"x"+str(height)+"+"+str(x)+"+"+str(y)
                    else:
                        width=config_geometria[0]
                        height=config_geometria[1]
                        x=top_level_position["x"]+top_level_size["width"]*config_geometria[2]
                        y=top_level_position["y"]+top_level_size["height"]*config_geometria[3]
                        self.geometria=str(int(width))+"x"+str(int(height))+"+"+str(int(x))+"+"+str(int(y))
            self.geometry(self.geometria)
            self.title(self.titulo)
        except Exception as e:
            print(str(e))
