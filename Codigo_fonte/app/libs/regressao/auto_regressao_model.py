from . import auto_regressao_lib
from .. import estatisticas
from ...processamento.exceptions.exception import tratamento_excessao,infoerroexception
from ...constantes import AUTO_REGRESSAO_ABR

class auto_regressao():

    #gets e sets

    def get_abreviacao(self):
        try:
            return AUTO_REGRESSAO_ABR
        except Exception as e:
            tratamento_excessao("Erro")

    def get_informacoes(self):
        try:
            self.dirt_informacoes={}
            self.dirt_informacoes["comprimento_sazonal"]=str(self.comprimento_sazonal)

            return self.dirt_informacoes
        except Exception as e:
            tratamento_excessao("Erro")

    def set_informacoes(self,dirt_informacoes):
        try:
            self.comprimento_sazonal=int(dirt_informacoes["comprimento_sazonal"])
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,serie_treinamento,series_previsao,model_fit=None):
        self.serie_treinamento=serie_treinamento[0]
        self.series_previsao=series_previsao
        self.model_fit=model_fit
        if(model_fit!=None):
            self.model_fited=True
        else:
            self.model_fited=False

    def fit_model(self,serie_treinamento=None,comprimento_sazonal=None):
        try:
            if(serie_treinamento!=None):
                self.serie_treinamento=serie_treinamento
            if(comprimento_sazonal==None):
                maior_autocorrelacao, comprimento_sazonal = serie_treinamento.get_best_sazonalidade()
                model_fit= auto_regressao_lib.fit(serie_treinamento.ploted_data_y, 144)
            self.comprimento_sazonal=comprimento_sazonal
            self.model_fit=model_fit
            self.model_fited=True
        except Exception as e:
            tratamento_excessao("Erro")

    def previsao(self,index_serie,comprimento_previsao,**kwargs):
        try:
            if(self.model_fited and index_serie<len(self.series_previsao)):
                serie_previsao_y=self.series_previsao[index_serie].ploted_data_y
                previsao_y= auto_regressao_lib.predict(self.model_fit,serie_previsao_y,len(serie_previsao_y),
                                                                   len(serie_previsao_y)+comprimento_previsao)
                previsao_y_rmse=auto_regressao_lib.predict(self.model_fit,serie_previsao_y,self.comprimento_sazonal,
                                                                                              len(serie_previsao_y))
                y_rmse=[serie_previsao_y[cont] for cont in range(self.comprimento_sazonal,len(serie_previsao_y))]
                rmse=estatisticas.RMSE(y_rmse,previsao_y_rmse)

                return previsao_y,rmse
            else:
                raise infoerroexception("Modelo ainda não treinado")
        except Exception as e:
            tratamento_excessao("Erro")

    def load_fited_model(self,url_model_file,**kwargs):
        try:
            self.model_fit=auto_regressao_lib.carregar_modelo(url_model_file)
            self.model_fited=True
        except Exception as e:
            tratamento_excessao("Erro")

    def save_fited_model(self,url_model_file):
        try:
            if(self.model_fited):
                auto_regressao_lib.salvar_modelo_ARResults(self.model_fit,url_model_file)
            else:
                raise infoerroexception("Modelo ainda não treinado")
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")