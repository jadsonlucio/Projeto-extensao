from . import OLS_lib
from .. import estatisticas
from ...constantes import OLS_ABR
from ...processamento.exceptions.exception import tratamento_excessao,infoerroexception

class OLS():

    #gets e sets

    def get_abreviacao(self):
        return OLS_ABR

    def get_informacoes(self):
        try:
            return OLS_lib.get_propriedades_modelo(self.model_fit)
        except Exception as e:
            tratamento_excessao("Erro")

    def set_informacoes(self,dirt_informacoes):
        try:
            self.comprimento_sazonal=int(dirt_informacoes["comprimento_sazonal"])
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,series_treinamento,series_previsao,serie_treinamento,model_fit=None):
        self.series_treinamento=series_treinamento
        self.serie_treinamento=serie_treinamento
        self.series_previsao=series_previsao
        self.model_fit=model_fit
        if(model_fit!=None):
            self.model_fited=True
        else:
            self.model_fited=False

    def fit_model(self,serie_treinamento=None,**kwargs):
            try:
                if (serie_treinamento != None):
                    self.serie_previsao = serie_treinamento

                array_series_treinamento=[serie.ploted_data_y for serie in self.series_treinamento]
                array_serie_previsao=serie_treinamento.ploted_data_y
                self.model_fit=OLS_lib.fit_model(array_series_treinamento,array_serie_previsao,**kwargs)
                self.model_fited=True
            except Exception as e:
                tratamento_excessao("Erro")

    def previsao(self,array_previsao,**kwargs):
        try:
            if(self.model_fited==True ):
                previsao=OLS_lib.predict(self.model_fit,array_previsao)
                return previsao,0
            else:
                raise infoerroexception("Modelo ainda não foi treinado")
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def save_fited_model(self,url_model_file):
        try:
            if(self.model_fited):
                OLS_lib.save_model(self.model_fit,url_model_file)
            else:
                raise infoerroexception("Modelo ainda não treinado")
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def load_fited_model(self,url_model_file,**kwargs):
        try:
            self.model_fit=OLS_lib.load_model(url_model_file)
            self.model_fited=True
        except Exception as e:
            tratamento_excessao("Erro")


