import numpy

from statsmodels import api
from statsmodels.tsa.ar_model import ARResults

from ...processamento.exceptions.exception import tratamento_excessao,infoerroexception

def fit(array,comprimento_sazonal,ic="aic"):
    try:
        if(comprimento_sazonal<len(array)):
            model=api.tsa.AR(array)
            model_fit=model.fit(maxlag=comprimento_sazonal)

            return model_fit
        else:
            raise infoerroexception("Comprimento sazonal maior que o tamanho da serie")
    except infoerroexception as e:
        tratamento_excessao("Info")
    except Exception as e:
        tratamento_excessao("Erro")

def predict(model,array,start,end):
    try:
        model.model.endog=numpy.reshape(numpy.array([valor for valor in array]),(1,len(array)))
        previsao=model.predict(start=start,end=end)
        return previsao
    except Exception as e:
        tratamento_excessao("Erro")

def salvar_modelo_ARResults(modelo,url_modelo):
    try:
        modelo.save(url_modelo)
    except Exception as e:
        tratamento_excessao("Erro")

def carregar_modelo(url_modelo):
    try:
        modelo=ARResults.load(url_modelo)
        return modelo
    except Exception as e:
        tratamento_excessao("Erro")