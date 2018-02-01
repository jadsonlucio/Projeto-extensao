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
            self.informacoes={}
            text_serie_treinamento=""
            tamanho_series_treinamento=len(self.series_treinamento)
            for cont in range(0,tamanho_series_treinamento):
                serie=self.series_treinamento[cont]
                if(cont<tamanho_series_treinamento-1):
                    text_serie_treinamento=text_serie_treinamento+serie.text_legenda+","
                else:
                    text_serie_treinamento = text_serie_treinamento + serie.text_legenda
            self.informacoes["Treinamento"]=text_serie_treinamento
            self.informacoes["Previsão"]=self.serie_treinamento.text_legenda
            dict_infos_model=OLS_lib.get_propriedades_modelo(self.model_fit)
            for key,arg in zip(dict_infos_model.keys(),dict_infos_model.values()):
                _key=key
                _arg=None
                if(isinstance(arg,float)):
                    _arg=round(arg,4)
                else:
                    new_array=[]
                    for valor in arg:
                        valor_arredondado=round(float(valor),4)
                        new_array.append(valor_arredondado)
                    _arg=str(new_array)

                self.informacoes[key]=_arg

            return self.informacoes
        except Exception as e:
            tratamento_excessao("Erro")

    def set_informacoes(self,dirt_informacoes):
        try:
            self.comprimento_sazonal=int(dirt_informacoes["comprimento_sazonal"])
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,series_treinamento,serie_treinamento,model_fit=None):
        self.series_treinamento=series_treinamento
        self.serie_treinamento=serie_treinamento
        self.model_fit=model_fit
        if(model_fit!=None):
            self.model_fited=True
        else:
            self.model_fited=False

    def fit_model(self,serie_treinamento=None,**kwargs):
            try:
                array_series_treinamento=[serie.ploted_data_y for serie in self.series_treinamento]
                array_serie_treinamento=serie_treinamento.ploted_data_y
                self.model_fit=OLS_lib.fit_model(array_series_treinamento,array_serie_treinamento,**kwargs)
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


