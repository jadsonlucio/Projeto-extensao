from ...processamento.exceptions.exception import tratamento_excessao,infoerroexception
from ..datas import converter_periodo,criar_array_date
from ..arquivo import criar_arquivo,salvar_array_arquivo
from ...libs import estatisticas

from ...constantes import EXTENSAO_SERIE
class serie_temporal():

    #funções geters e seters

    def set_tempo_serie(self,periodo=None,time_steps=None):
        if(periodo!=None):
            self.periodo=periodo
        if(time_steps!=None):
            self.time_steps=time_steps

    def get_estensao_serie(self):
        try:
            return EXTENSAO_SERIE
        except Exception as e:
            tratamento_excessao('Erro')

    def get_data_x(self,data_ploted=True):
        try:
            if(data_ploted):
                return self.ploted_data_x
            else:
                return self.data_x
        except Exception as e:
            tratamento_excessao("Erro")

    def get_data_y(self,data_ploted=True):
        try:
            if(data_ploted):
                return self.ploted_data_y
            else:
                return self.data_y
        except Exception as e:
            tratamento_excessao("Erro")

    def get_periodo(self,data_ploted=True):
        try:
            if(data_ploted):
                return self.ploted_periodo
            else:
                return self.periodo
        except Exception as e:
            tratamento_excessao("Erro")

    def get_time_steps(self,data_ploted=True):
        try:
            if(data_ploted):
                return self.ploted_time_steps
            else:
                return self.time_steps
        except Exception as e:
            tratamento_excessao("Erro")

    def get_date_serie(self,data_ploted=True):
        try:
            data_x=[]
            if(data_ploted):
                data_x=self.ploted_data_x
            else:
                data_x=self.data_x
            data_inicial=self.processamento.pre_processamento.data_inicial
            time_steps=self.processamento.pre_processamento.time_steps
            periodo=self.processamento.pre_processamento.periodo
            self.date_array=criar_array_date(data_x,data_inicial,periodo,time_steps)

            return self.date_array
        except Exception as e:
            tratamento_excessao("Erro")

    def get_name(self):
        try:
            self.name=self.text_legenda + " de " + str(self.date_inicial) + " a " + str(self.date_final)
            return self.name
        except Exception as e:
            tratamento_excessao("Erro")

    def get_estatisticas(self):
        try:
            dirt_estatisticas={}
            dirt_estatisticas["Média"]=round(self.media(self.is_ploted),2)
            dirt_estatisticas["Mediana"]=round(self.mediana(self.is_ploted),2)
            dirt_estatisticas["Moda"]=self.moda(self.is_ploted)
            dirt_estatisticas["Máximo"]=round(self.maximo(self.is_ploted)[0],2)
            dirt_estatisticas["Mínimo"]=round(self.minimo(self.is_ploted)[0],2)
            dirt_estatisticas["Amplitude"]=round(self.amplitude(self.is_ploted),2)
            dirt_estatisticas["Variância"]=round(self.variancia(self.is_ploted),2)
            dirt_estatisticas["Desvio padrão"]=round(self.desvio_padrao(self.is_ploted),2)

            return dirt_estatisticas
        except Exception as e:
            tratamento_excessao("Erro")

    def get_informacoes(self):
        try:
            self.dirt_informacoes={
                "Legenda":self.text_legenda,
                "Data":str(self.ploted_data_y),
                "Data inicial":str(self.date_inicial),
                "Data final":str(self.date_final),
                "Período":self.periodo,
                "Time steps":str(self.time_steps)
            }
            return self.dirt_informacoes
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,text_legenda,data_x, data_y, date_inicial, date_final, periodo, time_steps,processamento,pai=None):
        self.pai=pai
        self.text_legenda=text_legenda
        self.data_x = data_x
        self.data_y = data_y
        self.date_inicial = date_inicial
        self.date_final = date_final
        self.periodo = periodo
        self.time_steps = time_steps

        self.ploted_periodo = self.periodo
        self.ploted_time_steps = self.time_steps
        self.ploted_data_x = self.data_x
        self.ploted_data_y = self.data_y

        self.processamento = processamento

        self.line_2d=None
        self.subplot=None

        self.is_ploted=False
        self.is_visible=False
        self.is_select=False

        self.init_values={'data_x':self.data_x,'data_y':self.data_y,
                          'data_inicial':self.date_inicial,'data_final':self.date_final,'periodo'
                           :self.periodo,'time_steps':self.time_steps,'processamento':self.processamento}

    # funcõs de plotagem

    def plot(self, index_window=None, index_subplot=-1, plot_date=False,**kwargs):
        try:
            self.processamento.processamento_plot.plot_serie(self,index_subplot=index_subplot,plot_date=plot_date,**kwargs)
        except Exception as e:
            tratamento_excessao("Erro")

    # funções de tranformação data

    def mudar_tempo_serie(self,periodo,time_steps):
        try:
            tempo_serie_min=converter_periodo(self.periodo,'minuto')*self.time_steps
            tempo_serie_convertida=converter_periodo(periodo,'minuto')*time_steps
            constante = int(tempo_serie_convertida / tempo_serie_min)
            if(tempo_serie_min>tempo_serie_convertida or self.data_x[0]+constante>self.data_x[-1]):
                raise infoerroexception("Tempo a ser convertido\n e incompatível com o tempo da série")
            else:
                self.ploted_periodo=periodo
                self.ploted_time_steps=time_steps
                self.ploted_data_x=[self.data_x[valor] for valor in range(0,len(self.data_x),constante)]
                self.ploted_data_y=[self.data_y[valor] for valor in range(0,len(self.data_x),constante)]
        except infoerroexception as e:
            tratamento_excessao('Info')
        except Exception as e:
            tratamento_excessao('Erro')

    def converter_tempo(self,periodo,time_steps,data_ploted=True):
        try:
            periodo_serie=self.get_periodo(data_ploted)
            time_steps_serie=self.get_time_steps(data_ploted)
            tempo_convertido=converter_periodo(periodo,periodo_serie)*time_steps/time_steps_serie
            return tempo_convertido
        except Exception as e:
            tratamento_excessao("Erro")

    # funcões estatistica basica

    def maximo(self,data_ploted=True):
        if(data_ploted):
            return estatisticas.maximo(self.ploted_data_y)
        else:
            return estatisticas.maximo(self.data_y)

    def minimo(self,data_ploted=True):
        if(data_ploted):
            return estatisticas.minimo(self.ploted_data_y)
        else:
            return estatisticas.minimo(self.data_y)

    def amplitude(self,data_ploted=True):
        if(data_ploted):
            return estatisticas.amplitude(self.ploted_data_y)
        else:
            return estatisticas.amplitude(self.data_y)

    def media(self,data_ploted=True):
        if(data_ploted):
            return estatisticas.media(self.ploted_data_y)
        else:
            return estatisticas.media(self.data_y)

    def mediana(self,data_ploted=True):
        if (data_ploted):
            return estatisticas.mediana(self.ploted_data_y)
        else:
            return estatisticas.mediana(self.data_y)

    def moda(self,data_ploted=True):
        if (data_ploted):
            return estatisticas.moda(self.ploted_data_y)
        else:
            return estatisticas.moda(self.data_y)

    def variancia(self,data_ploted=True):
        if (data_ploted):
            return estatisticas.variancia(self.ploted_data_y)
        else:
            return estatisticas.variancia(self.data_y)

    def desvio_padrao(self,data_ploted=True):
        if (data_ploted):
            return estatisticas.desvio_padrao(self.ploted_data_y)
        else:
            return estatisticas.desvio_padrao(self.data_y)

    # funções transformação dados

    def regressao_linear(self,data_ploted=True):
        try:
            if(data_ploted):

                self.regressao_linear_x,self.regressao_linear_y=estatisticas.estatisticas_transf_serie.reta_tendencia(self.ploted_data_x,
                                                                                                                    self.ploted_data_y)
            else:
                self.regressao_linear_x, self.regressao_linear_y = estatisticas.estatisticas_transf_serie.reta_tendencia(self.data_x,
                                                                                                                         self.data_y)
            return self.regressao_linear_x,self.regressao_linear_y
        except Exception as e:
            tratamento_excessao("Erro")

    def media_movel_simples(self,lag,data_ploted=True):
        try:
            if(data_ploted):
                self.media_movel_x,self.media_movel_y=estatisticas.estatisticas_transf_serie.media_movel_simples(self.ploted_data_x,self.ploted_data_y,lag)
            else:
                self.media_movel_x, self.media_movel_y=estatisticas.estatisticas_transf_serie.media_movel_simples(self.data_x, self.data_y, lag)

            return self.media_movel_x,self.media_movel_y
        except Exception as e:
            tratamento_excessao("Erro")

    def media_movel_exponencial(self,const_regularizacao,data_ploted=True):
        try:
            if(data_ploted):
                self.media_movel_exp_x,self.media_movel_exp_y=estatisticas.estatisticas_transf_serie.ajuste_exponencial(self.ploted_data_x,
                                                                                                    self.ploted_data_y,const_regularizacao)
            else:
                self.media_movel_exp_x, self.media_movel_exp_y = estatisticas.estatisticas_transf_serie.ajuste_exponencial(self.data_x,
                                                                                                      self.data_y, const_regularizacao)

            return self.media_movel_exp_x,self.media_movel_exp_y
        except Exception as e:
            tratamento_excessao("Erro")

    def decomposicao(self,frequencia,modelo,data_ploted=True):
        try:
            self.decomposicao_info={
                "frequencia":frequencia,
                "modelo":modelo
            }
            if(data_ploted):
                data_x=self.ploted_data_x
                data_y=self.ploted_data_y
            else:
                data_x=self.data_x
                data_y=self.data_y
            tendencia, sazonalidade, ruido = estatisticas.decomposicao_serie(data_y, frequencia, modelo)
            self.decomposicao_info["tendencia_y"]=[]
            self.decomposicao_info["tendencia_x"]=[]
            self.decomposicao_info["sazonalidade_y"] = []
            self.decomposicao_info["sazonalidade_x"] = []
            self.decomposicao_info["ruido_y"] = []
            self.decomposicao_info["ruido_x"] = []
            for tendencia_valor,sazonalidade_valor,ruido_valor,x_valor in zip(tendencia,sazonalidade,ruido,data_x):
                if(str(tendencia_valor)!="nan"):
                    self.decomposicao_info["tendencia_x"].append(x_valor)
                    self.decomposicao_info["tendencia_y"].append(tendencia_valor)
                if(str(tendencia_valor)!="nan"):
                    self.decomposicao_info["sazonalidade_x"].append(x_valor)
                    self.decomposicao_info["sazonalidade_y"].append(sazonalidade_valor)
                if(str(tendencia_valor)!="nan"):
                    self.decomposicao_info["ruido_x"].append(x_valor)
                    self.decomposicao_info["ruido_y"].append(ruido_valor)
            return self.decomposicao_info

        except Exception as e:
            tratamento_excessao("Erro")

    def variacao(self,data_ploted=True):
        try:
            if(data_ploted):
                self.variacao_x,self.variacao_y=estatisticas.estatisticas_transf_serie.variacao(self.ploted_data_x,self.ploted_data_y)
            else:
                self.variacao_x,self.variacao_y=estatisticas.estatisticas_transf_serie.variacao(self.data_x,self.data_y)

            return self.variacao_x,self.variacao_y
        except Exception as e:
            tratamento_excessao("Erro")

    def remove_sazonality(self,termos_diferenciacoes=1):
        try:
            for cont in range(0,termos_diferenciacoes):
                new_array=[self.ploted_data_y[cont]-self.ploted_data_y[cont+1] for cont in range(len(self.ploted_data_y)-1)]
                self.ploted_data_y=new_array
        except Exception as e:
            tratamento_excessao("Erro")

    def autocorrelacao(self,termos_diferenciacoes=1,max_lag=None,data_ploted=True):
        if (data_ploted):
            serie = self.ploted_data_y
        else:
            serie = self.data_y
        if (termos_diferenciacoes == 1):
            new_serie = [serie[cont] - serie[cont + 1] for cont in range(len(serie) - 1)]
            serie = new_serie

        self.acf = estatisticas.Autocorrelacao(serie,nlags=max_lag)
        return self.acf

    def autocorrelacao_parcial(self,termos_diferenciacoes=1,max_lag=144,data_ploted=True):
        if (data_ploted):
            serie=self.ploted_data_y
        else:
            serie=self.data_y
        if (termos_diferenciacoes == 1):
            new_serie = [serie[cont] - serie[cont + 1] for cont in range(len(serie) - 1)]
            serie = new_serie
        self.pacf = estatisticas.Autocorrelacao_parcial(serie,nlags=max_lag)
        return self.pacf

    def get_best_sazonalidade(self,data_ploted=True,termos_diferenciacoes=1,max_lag=144,
                                      tipo_correlacao="pacf",porcentagem_acuracia="95%"):

        if (data_ploted):
            serie=self.ploted_data_y
        else:
            serie=self.data_y
        if (termos_diferenciacoes == 1):
            new_serie = [serie[cont] - serie[cont + 1] for cont in range(len(serie) - 1)]
            serie = new_serie
        return estatisticas.Get_best_sazonality(serie,tipo_correlacao=tipo_correlacao,porcentagem_acuracia=porcentagem_acuracia)

    # funções de transformação da serie

    def scale_serie(self,lim_superior,lim_inferior,data_ploted=True):
        try:
            if(not (isinstance(lim_superior,float) and isinstance(lim_inferior,float) and lim_superior>lim_inferior)):
                raise infoerroexception("Limite inferior maior ou igual ao limite superior")
            if(data_ploted):
                data_y=self.ploted_data_y
            else:
                data_y=self.data_y
            self.ploted_data_y=estatisticas.scale_array(data_y,lim_inferior,lim_superior)
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def reshape_serie(self,metodo_media,tam_intervalo,repetir_valores=False,data_ploted=True,**kwargs):
        try:
            if(data_ploted):
                data_x=self.ploted_data_x
                data_y=self.ploted_data_y
            else:
                data_x=self.data_x
                data_y=self.data_y
            self.ploted_data_x,self.ploted_data_y=estatisticas.estatisticas_transf_serie.reshape(data_x,
                                                    data_y,metodo_media,tam_intervalo,repetir_valores,**kwargs)

        except Exception as e:
            tratamento_excessao("Erro")

    # função criar menu

    def criar_menu(self):
        array=[]

    # funções de operações com series

    def save(self,nome_arquivo,caminho_arquivo=None,data_ploted=True):
        try:
            if(data_ploted):
                data_x=self.ploted_data_x
                data_y=self.ploted_data_y
                periodo=self.ploted_periodo
                time_steps=self.ploted_time_steps
            else:
                data_x = self.data_x
                data_y = self.data_y
                periodo = self.periodo
                time_steps = self.time_steps
            if(caminho_arquivo=="" or caminho_arquivo==None):
                raise infoerroexception("Nenhum diretorio selecionado")
            data_x="data_x="+str(data_x)
            data_y="data_y="+str(data_y)
            data_inicial="data_inicial="+str(self.date_inicial)
            data_final="data_final="+str(self.date_final)
            periodo="periodo="+self.periodo
            time_steps="time_steps="+str(self.time_steps)
            text_legenda="text_legenda="+self.text_legenda
            tipo_serie="tipo_serie="+"Normal"
            array=[data_x,data_y,data_inicial,data_final,periodo,time_steps,text_legenda,tipo_serie]
            salvar_array_arquivo(criar_arquivo(nome_arquivo+EXTENSAO_SERIE,caminho_arquivo),array)
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def __len__(self,data_ploted=True):
        try:
            if(data_ploted==True):
                if(self.is_ploted):
                    return len(self.ploted_data_y)
                else:
                    infoerroexception("Serie não esta plotada")
            else:
                return len(self.data_y)
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def __add__(self, other):
        return self.processamento.operacoes_series.somar_series(self,other)

    def __sub__(self, other):
        return self.processamento.operacoes_series.subtrair_series(self, other)

    def __mul__(self, other):
        return self.processamento.operacoes_series.multiplicar_series(self, other)

    def __truediv__(self, other):
        return self.processamento.operacoes_series.dividir_series(self, other)

class serie_analize():
    def __init__(self,tipo_serie,text_legenda,data_x, data_y, date_inicial, date_final,processamento,pai=None):
        self.tipo_serie=tipo_serie
        self.text_legenda=text_legenda
        self.data_x=data_x
        self.data_y=data_y
        self.data_inicial=date_inicial
        self.data_final=date_final
        self.processamento=processamento
        self.pai=pai

    def plot(self,index_window=None):
        if(self.tipo_serie=="bar"):
            pass

class serie_previsao(serie_temporal):
    def __init__(self,previsao,text_legenda,data_x, data_y, date_inicial,
                      date_final, periodo, time_steps,processamento,pai):
        self.previsao=previsao
        serie_temporal.__init__(self,text_legenda,data_x,data_y,date_inicial,date_final,periodo,time_steps,processamento,pai)


