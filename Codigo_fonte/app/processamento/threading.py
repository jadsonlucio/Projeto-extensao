from threading import Thread
from time import sleep

from .exceptions.exception import tratamento_excessao

threads=[]

class thread(Thread):
    def __init__(self, func, **kwargs):
        Thread.__init__(self)
        self.func = func
        self.kwargs = kwargs
        self.thread_ativa=False
    #rodar thread

    def run(self):
        try:
            self.thread_ativa=True
            self.func(**self.kwargs)
            self.thread_ativa=False
        except Exception as e:
            tratamento_excessao('Erro')


def criar_thread(func,**kwargs):
    thread_inst=thread(func,**kwargs)
    threads.append(thread_inst)
    thread_inst.start()
    return thread_inst