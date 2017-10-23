from matplotlib.lines import Line2D

from ..exceptions.exception import infoerroexception,tratamento_excessao
from ...instancias.Instancias import add_instancia,get_instancia
from ..series_temporais.series_temporais import serie_temporal,serie_analize,serie_previsao

from ..arquivo import abrir_arquivo,converter_array_to_dictonary,ler_array_arquivo
from ..datas import date

from ...libs import estatisticas

# Variaveis globais
instancias_processamento=[]

class processamento():
    #variaveis classe
    instancia_selecionada=None

    #geters e seters
    def get_time_serie(self,key,is_ploted=True):
        try:
            series=[]
            if(is_ploted):
                series=self.series_plotadas
            else:
                series=self.series_temporais
            if(isinstance(key,int)):
                return series[key]
            elif(isinstance(key,Line2D)):
                for serie in series:
                    if(serie.is_ploted):
                        if(serie.line_2d==key):
                            return serie
                return "linha_nao_encontrada"
            else:
                raise infoerroexception("opção invalida")
        except infoerroexception as e:
            tratamento_excessao('Info')
        except Exception as e:
            tratamento_excessao('Erro')

    def get_series_selecionadas(self):
        try:
            return self.series_selecionadas
        except Exception as e:
            tratamento_excessao('Erro')


    def __init__(self, frame_plot):
        self.frame_plot = frame_plot
        self.pre_processamento = get_instancia("pre_processamento")
        self.processamento_plot=processamento_plots(self)
        self.operacoes_series=operacoes_series(self)
        self.series_temporais = []
        self.series_analise=[]
        self.series_plotadas=[]
        self.series_selecionadas=[]

        instancias_processamento.append(self)

    # Funcões de verificacao

    def verificar_serie_plot(self,serie):
        try:
            for serie_plotada in self.series_plotadas:
                if(serie==serie_plotada):
                    return True
            return False
        except Exception as e:
            tratamento_excessao("Erro")

    def veirificar_serie_selecionada(self,serie):
        try:
            for serie_plotada in self.series_selecionadas:
                if(serie==serie_plotada):
                    return True
            return False
        except Exception as e:
            tratamento_excessao("Erro")

    def filtrar_series(self,tipos=None):
        try:
            series_selecionadas=[]
            if(tipos==None):
                return self.series_temporais
            else:
                for serie in self.series_temporais:
                    for tipo in tipos:
                        if(tipo=="normal" and isinstance(serie,serie_temporal) and not
                        isinstance(serie,serie_previsao) and not isinstance(serie,serie_analize)):
                            series_selecionadas.append(serie)
                        if(tipo=="previsao" and isinstance(serie,serie_previsao)):
                            series_selecionadas.append(serie)
                        if(tipo=="analize" and isinstance(serie,serie_analize)):
                            series_selecionadas.append(serie)
            return series_selecionadas
        except Exception as e:
            tratamento_excessao("Erro")

    # processamento graficos

    def _criar_serie_temporal(self, data_x, data_y, date_inicial, date_final, periodo=None,
                              time_steps=None,text_legenda=None, pai=None, tipo_serie='Normal',ignorar_save=False,**kwargs):
        if (tipo_serie == 'Normal'):
            serie = serie_temporal(text_legenda,data_x, data_y, date_inicial,
                                   date_final, periodo, time_steps, self, pai=None)
        elif(tipo_serie=="Previsao"):
            serie = serie_temporal(kwargs["previsao"],text_legenda, data_x, data_y, date_inicial,
                                   date_final, periodo, time_steps, self, pai=kwargs["pai"])
        if(ignorar_save==False):
            self.series_temporais.append(serie)
        return serie

    def _get_serie_data(self, data_inicial, data_final, index, **kwargs):
        return get_instancia("pre_processamento").get_simpletimeserie(data_inicial, data_final, index + 1, **kwargs)

    def _load_serie_temporal(self,url_arq_serie):
        try:
            kwargs=converter_array_to_dictonary(ler_array_arquivo(abrir_arquivo(url_arq_serie)))
            data_x=[float(valor) for valor in  kwargs["data_x"].split(",")]
            data_y=[float(valor) for valor in  kwargs["data_y"].split(",")]
            ano, mes, dia=[int(valor) for valor in kwargs["data_inicial"].split("-")]
            date_inicial=date(day=dia,month=mes,year=ano)
            ano, mes, dia = [int(valor) for valor in kwargs["data_final"].split("-")]
            date_final = date(day=dia, month=mes, year=ano)
            periodo=kwargs["periodo"]
            time_steps=int(kwargs["time_steps"])
            text_legenda=kwargs["text_legenda"]
            tipo_serie=kwargs["tipo_serie"]
            self._criar_serie_temporal( data_x, data_y, date_inicial, date_final, periodo,time_steps,text_legenda,)
        except Exception as e:
            tratamento_excessao("Erro")

    @classmethod
    def get_instancia_selecionada(cls):
        try:
            return cls.instancia_selecionada
        except Exception as e:
            tratamento_excessao("Erro")

    @classmethod
    def set_instancia_selecionada(cls,instancia):
        try:
            cls.instancia_selecionada=instancia
        except Exception as e:
            tratamento_excessao("Erro")


class processamento_plots():

    #geters e seters

    def excluir_series_plot(self,**kwargs):
        try:
            for serie in self.processamento.series_plotadas:
                self.excluir_plot_serie(serie,False)
            self.processamento.series_plotadas=[]
            self.processamento.series_selecionadas=[]
        except Exception as e:
            tratamento_excessao("Erro")

    def __init__(self,processamento):
        self.processamento=processamento

    def plot_serie(self,serie_temporal,update_screen=True,index_subplot=-1,plot_date=False,selecionar_serie=True,label_x="",label_y="",**plot_args):
        try:
            if (serie_temporal.processamento.verificar_serie_plot(serie_temporal)):
                if (self.processamento == serie_temporal.processamento):
                    serie_temporal.processamento.processamento_plot.excluir_plot_serie(serie_temporal,
                                                                                       update_screen=False)
                else:
                    serie_temporal.processamento.processamento_plot.excluir_plot_serie(serie_temporal,
                                                                                       update_screen=True)
                    serie_temporal.processamento=self.processamento

            if (serie_temporal.text_legenda != None):
                self.processamento.frame_plot.botao_aba.text_var.set(serie_temporal.text_legenda)
            if(plot_date):
                data_x=serie_temporal.get_date_serie()
            else:
                data_x=serie_temporal.ploted_data_x

            line_2d, subplot = self.processamento.frame_plot.plot_normal(data_x,
                                                                         serie_temporal.ploted_data_y, label_x,
                                                                         label_y, index_subplot, **plot_args)
            serie_temporal.line_2d = line_2d
            serie_temporal.subplot = subplot
            serie_temporal.is_ploted = True
            serie_temporal.is_visible = True
            if(not self.processamento.verificar_serie_plot(serie_temporal)):
                self.processamento.series_plotadas.append(serie_temporal)
            if(selecionar_serie==True ):
                self.selecionar_serie(serie_temporal,update_screen=False)
            if(update_screen==True):
                self.processamento.frame_plot.update_screen()
        except Exception as e:
            tratamento_excessao("Erro")

    def box_plot(self,serie_temporal,periodo,time_steps,update_screen=True,**plot_args):
        try:
            data=serie_temporal.reshape_periodo(periodo,time_steps)
            self.processamento.frame_plot.box_plot(data)
            if (update_screen == True):
                self.processamento.frame_plot.update_screen()
        except Exception as e:
            tratamento_excessao("Erro")

    def plot_autocorrelacao(self,serie_temporal,tipo_plot="pacf",titulo="",alpha=0.05,lags=None,update_screen=True,**plot_args):
        self.excluir_series_plot()
        self.processamento.frame_plot.plot_autocorrelacao(serie_temporal.ploted_data_y,titulo,tipo_plot,lags,alpha,**plot_args)
        if (update_screen == True):
            self.processamento.frame_plot.update_screen()

    def plot_correlacao(self,serie_1,serie_2,update_screen=True,**plot_args):
        self.excluir_series_plot()
        self.processamento.frame_plot.plot_scatter(serie_1.ploted_data_y,serie_2.ploted_data_y,**plot_args)
        if (update_screen == True):
            self.processamento.frame_plot.update_screen()

    def plot_histograma(self,serie_temporal,quantidade_classes,normalizar_dados=False,update_screen=True,**plot_args):
        text_label="Histograma "+serie_temporal.text_legenda
        self.processamento.frame_plot.plot_histograma(serie_temporal.ploted_data_y,quantidade_classes,normalizar_dados,label=text_label)
        if (update_screen == True):
            self.processamento.frame_plot.update_screen()


    def excluir_plot_serie(self,serie_temporal,update_screen=True):
        try:
            if(self.processamento.verificar_serie_plot(serie_temporal)):
                serie_temporal.is_visible=False
                serie_temporal.is_ploted=False
                serie_temporal.is_select=False
                serie_temporal.line_2d.remove()
                self.processamento.series_plotadas.remove(serie_temporal)
            else:
                raise infoerroexception("A serie não esta plotada")
            if(self.processamento.veirificar_serie_selecionada(serie_temporal)):
                self.processamento.series_selecionadas.remove(serie_temporal)
            if(update_screen==True):
                self.processamento.frame_plot.update_screen()
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def selecionar_serie(self,serie_temporal,update_screen=True,resetar_series_selecionadas=True):
        try:
            if(self.processamento.verificar_serie_plot(serie_temporal)):
                if(resetar_series_selecionadas):
                    for serie in self.processamento.series_selecionadas:
                        serie.is_select=False
                        serie.line_2d.set_alpha(0.3)
                    self.processamento.series_selecionadas = []

                if(not serie_temporal.is_select):
                    serie_temporal.is_select = True
                    serie_temporal.line_2d.set_alpha(1.0)
                    if (not self.processamento.veirificar_serie_selecionada(serie_temporal)):
                        self.processamento.series_selecionadas.append(serie_temporal)
                else:
                    serie_temporal.is_select = False
                    serie_temporal.line_2d.set_alpha(0.3)
                    if (self.processamento.veirificar_serie_selecionada(serie_temporal)):
                        self.processamento.series_selecionadas.remove(serie_temporal)
            else:
                print("A serie não esta plotada")
            if(update_screen==True):
                self.processamento.frame_plot.update_screen()
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def move_plot_serie(self,serie_temporal,index_subplot,update_screen=True):
        try:
            if(self.processamento.verificar_serie_plot(serie_temporal)):
                serie_temporal.plot(index_subplot=index_subplot,label=serie_temporal.text_legenda)
            else:
                raise infoerroexception("A serie não esta plotada")
            if(update_screen==True):
                self.processamento.frame_plot.update_screen()
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def mudar_visibilidade_plot_serie(self,serie_temporal,update_screen=True):
        try:
            if (self.processamento.verificar_serie_plot(serie_temporal)):
                serie_temporal.line_2d.set_visible(not serie_temporal.line_2d.get_visible())
                serie_temporal.is_visible=False
            else:
                raise infoerroexception("A serie não esta plotada")
            if (update_screen == True):
                self.processamento.frame_plot.update_screen()
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

class operacoes_series():

    def __init__(self,processamento):
        self.processamento=processamento

    def operacao_series(self,serie_x,serie_y,operador,**kwargs):
        try:
            datay_serie_x = serie_x.get_data_y(serie_x.is_ploted)
            if(isinstance(serie_y,serie_temporal)):
                datay_serie_y = serie_y.get_data_y(serie_y.is_ploted)
            elif(isinstance(serie_y,float)):
                datay_serie_y = [serie_y for cont in range(0,len(datay_serie_x))]
            else:
                raise infoerroexception("Tipos de dados imcompativeis")
            if(len(datay_serie_x)==len(datay_serie_y)):
                resultado=[]
                for valor_1,valor_2 in zip(datay_serie_x,datay_serie_y):
                    if(operador=="soma" or operador=="+"):
                        resultado.append(valor_1+valor_2)
                    elif(operador=="subtração" or operador=="-"):
                        resultado.append(valor_1 - valor_2)
                    elif(operador=="multiplicação" or operador=="x" or operador=="*"):
                        resultado.append(valor_1 * valor_2)
                    elif(operador=="divisão" or operador=="/" ):
                        resultado.append(valor_1/valor_2)
            else:
                raise infoerroexception("As series devem possuir o mesmo tamanho")
            serie_final=self.processamento._criar_serie_temporal(serie_x.get_data_x(serie_x.is_ploted),resultado,serie_x.date_inicial,serie_x.date_final,
                                       serie_x.get_periodo(serie_x.is_ploted),serie_x.get_time_steps(serie_x.is_ploted),"Soma")
            return serie_final
        except infoerroexception as e:
            tratamento_excessao("Info")
        except Exception as e:
            tratamento_excessao("Erro")

    def somar_series(self,serie_x,serie_y,**kwargs):
        return self.operacao_series(serie_x,serie_y,operador="soma")

    def subtrair_series(self,serie_x,serie_y,**kwargs):
        return self.operacao_series(serie_x,serie_y,operador="subtração")

    def multiplicar_series(self,serie_x,serie_y,**kwargs):
        return self.operacao_series(serie_x,serie_y,operador="multiplicação")

    def dividir_series(self,serie_x,serie_y,**kwargs):
        return self.operacao_series(serie_x,serie_y,operador="divisão")

    #funções de criação de series trasformadas

    def regressao_linear(self,serie_temporal,plot=True):
        try:
            data_x,data_y=serie_temporal.regressao_linear(serie_temporal.is_ploted)
            new_serie_temporal=self.processamento._criar_serie_temporal(data_x,data_y,serie_temporal.date_inicial,
                               serie_temporal.date_final,serie_temporal.ploted_periodo,serie_temporal.ploted_time_steps,
                                "Regressão Linear:"+serie_temporal.text_legenda,pai=serie_temporal,tipo_serie="Normal")
            if(plot):
                new_serie_temporal.plot(label="RL:"+serie_temporal.text_legenda)
            return new_serie_temporal

        except Exception as e:
            tratamento_excessao("Erro")

    def media_movel_simples(self,serie_temporal,lag,plot=True):
        try:
            data_x,data_y=serie_temporal.media_movel_simples(lag,serie_temporal.is_ploted)
            new_serie_temporal=self.processamento._criar_serie_temporal(data_x,data_y,serie_temporal.date_inicial,
                               serie_temporal.date_final,serie_temporal.ploted_periodo,serie_temporal.ploted_time_steps,
                                "Média Móvel:"+serie_temporal.text_legenda,pai=serie_temporal,tipo_serie="Normal")
            if(plot):
                new_serie_temporal.plot(label="MMS:"+serie_temporal.text_legenda)
            return new_serie_temporal
        except Exception as e:
            tratamento_excessao("Erro")

    def media_movel_exponencial(self,serie_temporal,const_regularizacao,plot=True):
        try:
            data_x,data_y=serie_temporal.media_movel_exponencial(const_regularizacao,serie_temporal.is_ploted)
            new_serie_temporal=self.processamento._criar_serie_temporal(data_x,data_y,serie_temporal.date_inicial,
                               serie_temporal.date_final,serie_temporal.ploted_periodo,serie_temporal.ploted_time_steps,
                                "Média Móvel:"+serie_temporal.text_legenda,pai=serie_temporal,tipo_serie="Normal")
            if(plot):
                new_serie_temporal.plot(label="MME:"+serie_temporal.text_legenda)
            return new_serie_temporal
        except Exception as e:
            tratamento_excessao("Erro")

    def variacao(self,serie_temporal,plot=True):
        try:
            data_x,data_y=serie_temporal.variacao(serie_temporal.is_ploted)
            new_serie_temporal=self.processamento._criar_serie_temporal(data_x,data_y,serie_temporal.date_inicial,
                               serie_temporal.date_final,serie_temporal.ploted_periodo,serie_temporal.ploted_time_steps,
                                "Variação:"+serie_temporal.text_legenda,pai=serie_temporal,tipo_serie="Normal")
            if(plot):
                new_serie_temporal.plot(label="VR:"+serie_temporal.text_legenda)
            return new_serie_temporal
        except Exception as e:
            tratamento_excessao("Erro")

    def decomposicao(self,serie_temporal,metrica,modelo,frequencia,plot=True):
        try:
            sigla=""
            metrica=metrica

            if(metrica==0 or metrica=="Tendência"):
                metrica="tendencia"
                sigla="T"
            if(metrica==1 or metrica=="Sazonalidade"):
                metrica="sazonalidade"
                sigla="S"
            if(metrica==2 or metrica=="Ruido"):
                metrica="ruido"
                sigla="R"

            decomposicao=serie_temporal.decomposicao(frequencia,modelo,serie_temporal.is_ploted)
            new_serie_temporal=self.processamento._criar_serie_temporal(decomposicao[metrica+"_x"],decomposicao[metrica+"_y"],
                               serie_temporal.date_inicial,serie_temporal.date_final,serie_temporal.ploted_periodo,serie_temporal.ploted_time_steps,
                                                                    metrica+":"+serie_temporal.text_legenda,pai=serie_temporal,tipo_serie="Normal")
            if(plot):
                new_serie_temporal.plot(label=sigla+":"+serie_temporal.text_legenda)
            return new_serie_temporal
        except Exception as e:
            tratamento_excessao("Erro")

# Processamento geral

def get_time_series(index_janela=None):
    try:
        pass
    except Exception as e:
        tratamento_excessao("Erro")

