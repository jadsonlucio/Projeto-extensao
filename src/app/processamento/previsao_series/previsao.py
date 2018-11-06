from ..exceptions.exception import tratamento_excessao,infoerroexception
from ..arquivo import converter_dictonary_to_array,converter_array_to_dictonary,\
                      criar_arquivo,salvar_array_arquivo,create_dir,abrir_arquivo,ler_array_arquivo,split_url

from ..series_temporais.processamento import processamento
from ..datas import converter_periodo,converter_string_to_date,operacao_datas
from ...instancias.Instancias import get_instancia
from ...constantes import EXTENSAO_MODELOS_PREVISAO,EXTENSAO_PREVISAO,EXTENSAO_SERIE,EXTENSAO_INFORMACOES_MODELO

from ...libs.regressao.auto_regressao_model import auto_regressao
from ...libs.holtwinters.holtwinters_model import holtwinters
from ...libs.MLP.mlp_model import rede_neural


array_previsao=[]

class previsao():

    #gets e sets

    def get_extensao_model(self):
        try:
            return EXTENSAO_MODELOS_PREVISAO
        except Exception as e:
            tratamento_excessao("Erro")

    def get_informacoes(self):
        try:
            self.dirt_informacoes={}
            self.dirt_informacoes["tipo_previsao"]=self.tipo_previsao
            self.dirt_informacoes["series_treinamento"]=""
            self.dirt_informacoes["series_previsao"]=""
            self.dirt_informacoes["serie_previsao"]=""
            self.dirt_informacoes["nome_arquivo_previsao"]="previsao"+EXTENSAO_PREVISAO
            self.dirt_informacoes["nome_arquivo_modelo"]="modelo"+EXTENSAO_MODELOS_PREVISAO
            self.dirt_informacoes["nome_arquivo_informacoes_modelo"]="modelo_infos"+EXTENSAO_INFORMACOES_MODELO

            for serie in self.series_treinamento:
                self.dirt_informacoes["series_treinamento"]=self.dirt_informacoes["series_treinamento"]+"treinamento "+serie.get_name()+","
            for serie in self.series_previsao:
                self.dirt_informacoes["series_previsao"]=self.dirt_informacoes["series_previsao"]+"previsao "+serie.get_name()+","

            if(self.serie_previsao!=None):
                self.dirt_informacoes["serie_previsao"]="previsao "+self.serie_previsao.get_name()

            return self.dirt_informacoes

        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,tipo_previsao,parametros_previsao=None,series_treinamento=None,series_previsao=None,serie_previsao=None,**kwargs):
        try:
            self.tipo_previsao=tipo_previsao
            self.series_treinamento=series_treinamento
            self.series_previsao=series_previsao
            self.parametros_previsao=parametros_previsao
            if(isinstance(serie_previsao,list)):
                self.serie_previsao = serie_previsao[0]
            else:
                self.serie_previsao=serie_previsao

            if(tipo_previsao=="Holt-winters Aditivo" or tipo_previsao=="Holt-winters Multiplicativo" or tipo_previsao=="Holt-winters Linear"):
                if(len(series_treinamento)==1 and len(series_previsao)>0):
                    self.model=holtwinters(tipo_previsao,series_treinamento,series_previsao,parametros_previsao)
                elif(len(series_treinamento)==0 or len(series_previsao)==0):
                    raise infoerroexception("Não existem séries de treinamento/previsão,\n por favor adicione-as para continuar")
                elif(len(series_treinamento)>0):
                    raise infoerroexception("Este modelo não aceita mais de uma série como treinamento,\n por favor reduza o tamanho "
                                            "das series para uma")

            elif(tipo_previsao=="Regressão"):
                if(len(series_treinamento)==1 and len(series_previsao)>0):
                    self.model=auto_regressao(series_treinamento,series_previsao,parametros_previsao)
                elif(len(series_treinamento)==0 or len(series_previsao)==0):
                    raise infoerroexception("Não existem series de treinamento/previsao,\n por favor as adicione para continuar")
                elif(len(series_treinamento)>1):
                    raise infoerroexception("Este modelo não aceita mais de uma série como treinamento,\n por favor reduza o tamanho "
                                            "das series para uma")

            elif(tipo_previsao=="Rede neural"):
                if(len(series_treinamento)>0 and serie_previsao!=None):
                    self.model=rede_neural(self.series_treinamento,self.series_previsao,self.serie_previsao,self.parametros_previsao)
                elif(len(series_treinamento)==0 or serie_previsao==None):
                    raise infoerroexception("Não existem series de treinamento/previsao,\n por favor as adicione para continuar")
                elif(len(serie_previsao)>1):
                    raise infoerroexception("Este modelo não aceita mais de uma série como treinamento,\n por favor reduza o tamanho "
                                            "das series para uma")

            else:
                raise infoerroexception("Tipo de previsão invalida")
            add_previsao(self)
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def prever_serie(self,index_serie_previsao,data_previsao):
        try:
            if(isinstance(index_serie_previsao,int)):
                serie_previsao=self.series_previsao[index_serie_previsao]
            else:
                serie_previsao=index_serie_previsao
            if(isinstance(data_previsao,str)):
                data_previsao = converter_string_to_date(data_previsao, "/")
            else:
                data_previsao=data_previsao
            pre_processamento = get_instancia("pre_processamento")
            periodo_time_staps_convertido = converter_periodo(serie_previsao.ploted_periodo,pre_processamento.periodo) * serie_previsao.ploted_time_steps / pre_processamento.time_steps
            quant_dias_previsao = operacao_datas("-", serie_previsao.date_final, data_previsao)
            quant_valores_previstos = int(converter_periodo("dia",serie_previsao.ploted_periodo) * quant_dias_previsao / serie_previsao.ploted_time_steps)

            data_y,rmse=self.model.previsao(index_serie_previsao,quant_valores_previstos)
            data_x=[serie_previsao.ploted_data_x[-1] + cont * periodo_time_staps_convertido for cont in range(len(data_y))]

            inst_processamento=processamento.get_instancia_selecionada()
            inst_processamento._criar_serie_temporal(data_x,data_y,serie_previsao.date_final,data_previsao,
                                                     serie_previsao.ploted_periodo,serie_previsao.ploted_time_steps
                                                     ,self.model.get_abreviacao()+":"+serie_previsao.text_legenda)

            serie_prevista = inst_processamento.series_temporais[-1]
            return serie_prevista

        except Exception as e:
            tratamento_excessao("Erro")

    def save(self,url_file):
        try:
            self.diretorio_previsao = url_file +"Modelo previsão "+self.tipo_previsao+"//"
            create_dir(self.diretorio_previsao)
            informacoes_previsao=self.get_informacoes()
            array_informacoes_previsao=converter_dictonary_to_array(informacoes_previsao)
            arquivo_infos_previsao=criar_arquivo(informacoes_previsao["nome_arquivo_previsao"],self.diretorio_previsao)
            salvar_array_arquivo(arquivo_infos_previsao,array_informacoes_previsao)

            self.save_series(self.series_treinamento,informacoes_previsao["series_treinamento"].split(',')[:-1],
                             self.diretorio_previsao)
            self.save_series(self.series_previsao, informacoes_previsao["series_previsao"].split(',')[:-1],
                             self.diretorio_previsao)
            if(self.model.model_fited):
                informacoes_modelo = self.model.get_informacoes()
                array_informacoes_modelo = converter_dictonary_to_array(informacoes_modelo)
                arquivo_infos_model = criar_arquivo(informacoes_previsao["nome_arquivo_informacoes_modelo"],
                                                       self.diretorio_previsao)
                salvar_array_arquivo(arquivo_infos_model, array_informacoes_modelo)
                self.model.save_fited_model(self.diretorio_previsao+"//"+informacoes_previsao["nome_arquivo_modelo"])
        except Exception as e:
            tratamento_excessao("Erro")

    def save_series(self,series,array_nomes,url):
        try:
            for serie,nome in zip(series,array_nomes):
                serie.save(nome,url)

        except Exception as e:
            tratamento_excessao("Erro")

def add_previsao(previsao):
    try:
        array_previsao.append(previsao)
    except Exception as e:
        tratamento_excessao("Erro")

def remover_previsao(previsao):
    try:
        encontrou=False
        for instancia_previsao in array_previsao:
            if(previsao==instancia_previsao):
                encontrou=True
                del instancia_previsao
        if(not encontrou):
            raise infoerroexception("Instancia de previsão não encontrada")
    except Exception as e:
        tratamento_excessao("Erro")

def load_previsao(url_arquivo_previsao):
    try:
        arquivo=abrir_arquivo(url_arquivo_previsao)
        array_informacoes_previsao=ler_array_arquivo(arquivo)
        dirt_informacoes_previsao=converter_array_to_dictonary(array_informacoes_previsao)
        dirt_url_arquivo_previsao=split_url(url_arquivo_previsao)

        series_treinamento=[]
        series_previsao=[]
        serie_previsao=None
        model_geometry=None

        url_series=dirt_url_arquivo_previsao["url_file"]
        url_model=dirt_url_arquivo_previsao["url_file"]
        url_model_info=dirt_url_arquivo_previsao["url_file"]

        inst_processamento=processamento.instancia_selecionada

        for serie_treinamento_name in dirt_informacoes_previsao["series_treinamento"].split(',')[:-1]:
            inst_processamento._load_serie_temporal(url_series+serie_treinamento_name+EXTENSAO_SERIE)
            series_treinamento.append(inst_processamento.series_temporais[-1])

        for serie_previsao_name in dirt_informacoes_previsao["series_previsao"].split(',')[:-1]:
            inst_processamento._load_serie_temporal(url_series+serie_previsao_name+EXTENSAO_SERIE)
            series_previsao.append(inst_processamento.series_temporais[-1])

        arquivo_informacoes_modelo=abrir_arquivo(url_model_info+dirt_informacoes_previsao["nome_arquivo_informacoes_modelo"])
        array_informacoes_modelo=ler_array_arquivo(arquivo_informacoes_modelo)
        dirt_informacoes_modelo=converter_array_to_dictonary(array_informacoes_modelo)

        if (len(dirt_informacoes_previsao["serie_previsao"])>0):
            inst_processamento._load_serie_temporal(url_series + dirt_informacoes_previsao["serie_previsao"] + EXTENSAO_SERIE)
            serie_previsao = inst_processamento.series_temporais[-1]

        previsao_carregada=previsao(dirt_informacoes_previsao["tipo_previsao"],None,series_treinamento,series_previsao,serie_previsao)
        previsao_carregada.model.load_fited_model(url_model+dirt_informacoes_previsao["nome_arquivo_modelo"])
        previsao_carregada.model.set_informacoes(dirt_informacoes_modelo)



        return previsao_carregada
    except Exception as e:
        tratamento_excessao("Erro")
