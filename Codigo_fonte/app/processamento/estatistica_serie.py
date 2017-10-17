from .exceptions.exception import tratamento_excessao,infoerroexception
from ..processamento.arquivo import criar_arquivo,join_dirt,converter_dictonary_to_array,salvar_array_arquivo
from ..constantes import EXTENSAO_ESTATISTICA_SERIE
from ..libs import estatisticas

estatisticas_series=[]

class estatistica_serie():

    #gets e sets
    def set_estatisticas(self):
        try:
            self.estatisticas=self.serie_temporal.get_estatisticas()
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,serie_temporal):
        self.serie_temporal=serie_temporal
        self.estatisticas={}

    def salvar_estatistica(self,url_arquivo):
        try:
            informacoes_serie=self.serie_temporal.get_informacoes()
            nome_arquivo=self.serie_temporal.get_name()+EXTENSAO_ESTATISTICA_SERIE
            arquivo=criar_arquivo(nome_arquivo,url_arquivo)
            dirt_arquivo=join_dirt(informacoes_serie,self.estatisticas)
            array_arquivo=converter_dictonary_to_array(dirt_arquivo)
            salvar_array_arquivo(arquivo,array_arquivo)

        except Exception as e:
            tratamento_excessao("Erro")

def criar_estatistica(serie_temporal):
    try:
        serie_encontrada=False
        for estatistica in estatisticas_series:
            if(estatistica.serie_temporal==serie_temporal):
                serie_encontrada=True
        if(serie_encontrada==False):
            estatisticas_series.append(estatistica_serie(serie_temporal))
    except Exception as e:
        tratamento_excessao("Erro")