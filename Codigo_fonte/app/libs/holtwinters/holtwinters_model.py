from . import holtwinters_lib
from .. import estatisticas
from ...processamento.exceptions.exception import tratamento_excessao,infoerroexception
from ...processamento.arquivo import abrir_arquivo,ler_array_arquivo,converter_array_to_dictonary,\
                                                        criar_arquivo,salvar_array_arquivo,split_url
from ...constantes import HOLT_WINTES_ABR

class holtwinters():

    def get_abreviacao(self):
        try:
            return HOLT_WINTES_ABR
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

    def __init__(self,holtwinters_name,serie_treinamento,series_previsao,model_fit=None):
        self.tipo_holtwinters=holtwinters_name
        self.serie_treinamento=serie_treinamento[0]
        self.series_previsao=series_previsao
        self.model_fit=model_fit
        if(model_fit!=None):
            self.model_fited=True
        else:
            self.model_fited=False
        self.previsoes=[]

    def run_model(self,serie_temporal,comprimento_previsao=1,comprimento_sazonal=None,alpha=None,beta=None,gama=None):
        try:
            self.comprimento_sazonal=comprimento_sazonal
            if(self.tipo_holtwinters=="Holt-winters Aditivo"):
                if(self.serie_treinamento.is_ploted):
                    previsao,alpha,beta,gama,rmse= holtwinters_lib.additive(serie_temporal.ploted_data_y, comprimento_sazonal,
                                                                            comprimento_previsao, alpha, beta, gama)
                else:
                    previsao, alpha, beta, gama, rmse = holtwinters_lib.additive(serie_temporal.data_y, comprimento_sazonal,
                                                                                 comprimento_previsao, alpha, beta, gama)
            elif(self.tipo_holtwinters=='Holt-winters Multiplicativo'):
                if (self.serie_treinamento.is_ploted):
                    previsao, alpha, beta, gama, rmse = holtwinters_lib.multiplicative(serie_temporal.ploted_data_y,
                                                                                       comprimento_sazonal, comprimento_previsao, alpha, beta, gama)
                else:
                    previsao, alpha, beta, gama, rmse = holtwinters_lib.multiplicative(serie_temporal.data_y,
                                                                                       comprimento_sazonal, comprimento_previsao, alpha, beta, gama)
            elif(self.tipo_holtwinters=='Holt-winters Linear'):
                if (self.serie_treinamento.is_ploted):
                    previsao, alpha, beta, rmse = holtwinters_lib.linear(serie_temporal.ploted_data_y,
                                                                         comprimento_previsao, alpha, beta)
                else:
                    previsao, alpha, beta, rmse = holtwinters_lib.linear(serie_temporal.data_y,
                                                                         comprimento_previsao, alpha, beta)
            else:
                raise infoerroexception("Tipo não encontrado")

            return previsao, alpha, beta, gama, rmse

        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def fit_model(self,serie_treinamento=None,comprimento_sazonal=None):
        try:

            if(serie_treinamento!=None):
                self.serie_treinamento=serie_treinamento
            if(comprimento_sazonal==None):
                maior_autocorrelacao,comprimento_sazonal=serie_treinamento.get_best_sazonalidade()
                print("maior comprimento_sazonal:"+str(comprimento_sazonal))
            _,alpha,beta,gama,rmse=self.run_model(self.serie_treinamento,1,comprimento_sazonal)
            self.comprimento_sazonal=comprimento_sazonal
            self.alpha=alpha
            self.beta=beta
            self.gama=gama
            self.model_fit=[alpha,beta,gama]
            self.rmse=rmse
            self.model_fited=True
            return rmse
        except Exception as e:
            tratamento_excessao("Erro")

    def previsao(self,index_serie,comprimento_previsao,**kwargs):
        try:
            if(self.model_fited and index_serie<len(self.series_previsao)):
                alpha,beta,gama=self.model_fit[0],self.model_fit[1],self.model_fit[2]
                previsao,_,_,_,rmse=self.run_model(self.series_previsao[index_serie],comprimento_previsao,self.comprimento_sazonal,
                                                   alpha,beta,gama)
                return previsao,rmse
            else:
                raise infoerroexception("Modelo ainda não foi treinado")
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")


    def load_fited_model(self,url_model_file,**kwargs):
        try:
            arquivo=abrir_arquivo(url_model_file)
            dirt=converter_array_to_dictonary(ler_array_arquivo(arquivo))
            self.model_fit=[float(dirt["alpha"]),float(dirt["beta"]),float(dirt["gama"])]
            self.model_fited=True
        except Exception as e:
            tratamento_excessao("Erro")

    def save_fited_model(self,url_model_file):
        try:
            if(self.model_fited):
                dirt_url_model=split_url(url_model_file)
                arquivo_model=criar_arquivo(dirt_url_model["file_name"]+dirt_url_model["file_extension"],dirt_url_model["url_file"]+"//")
                array_model=["alpha="+str(self.model_fit[0]),"beta="+str(self.model_fit[1]),"gama="+str(self.model_fit[2])]
                salvar_array_arquivo(arquivo_model,array_model)
            else:
                raise infoerroexception("Modelo ainda não treinado")
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")


