from . import mlp_lib
from .. import estatisticas
from ...constantes import REDE_NEURAL_MLP_ABR
from ...processamento.exceptions.exception import tratamento_excessao,infoerroexception

class rede_neural():

    #gets e sets

    def get_abreviacao(self):
        return REDE_NEURAL_MLP_ABR

    def get_informacoes(self):
        try:
            self.dirt_informacoes=self.model_fit.get_params()
            self.dirt_informacoes["comprimento_sazonal"]=str(self.comprimento_sazonal)

            return self.dirt_informacoes
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

    def fit_model(self,serie_treinamento=None,comprimento_sazonal=None):
            try:
                if (serie_treinamento != None):
                    self.serie_previsao = serie_treinamento
                if (comprimento_sazonal == None):
                    maior_autocorrelacao, comprimento_sazonal = serie_treinamento.get_best_sazonalidade()

                self.comprimento_sazonal=comprimento_sazonal
                self.comprimento_saida=comprimento_sazonal
                self.geometry_camadas_intermediarias=[40]

                array_series_treinamento=[serie.ploted_data_y for serie in self.series_treinamento]
                array_serie_previsao=serie_treinamento.ploted_data_y
                self.model_fit=mlp_lib.fit(array_series_treinamento,array_serie_previsao,self.geometry_camadas_intermediarias,
                                                                              self.comprimento_sazonal,self.comprimento_saida)
                self.model_fited=True
            except Exception as e:
                tratamento_excessao("Erro")

    def previsao(self,index_serie,comprimento_previsao,**kwargs):
        try:
            if(self.model_fited==True and index_serie<len(self.series_previsao)):
                serie_selecionada=self.series_previsao[index_serie]
                previsao=mlp_lib.predict(self.model_fit,serie_selecionada.ploted_data_y,comprimento_previsao,self.comprimento_sazonal)
                return previsao,0
            if(index_serie<len(self.series_previsao)):
                raise infoerroexception("Série não encontrada")
            else:
                raise infoerroexception("Modelo ainda não foi treinado")
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def save_fited_model(self,url_model_file):
        try:
            if(self.model_fited):
                mlp_lib.save_model(self.model_fit,url_model_file)
            else:
                raise infoerroexception("Modelo ainda não treinado")
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def load_fited_model(self,url_model_file,**kwargs):
        try:
            self.model_fit=mlp_lib.load_model(url_model_file)
            self.model_fited=True
        except Exception as e:
            tratamento_excessao("Erro")


