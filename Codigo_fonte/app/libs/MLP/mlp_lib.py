import numpy
import pickle

from sklearn.neural_network import MLPRegressor
from app.libs import estatisticas

from ...processamento.exceptions.exception import tratamento_excessao,infoerroexception
from ...processamento.arquivo import criar_arquivo,salvar_array_arquivo
numpy.random.seed(7)

def salvar_arquivo_treinamento(array_treinamento):
    try:
        arquivo=criar_arquivo("treinamento_rede_neural","app//")
        salvar_array_arquivo(arquivo,array_treinamento)
    except Exception as e:
        print(str(e))

def criar_treinamento(array_entrada, array_saida, tamanho_entrada, tamanho_saida):
    try:
        trainX=[]
        trainY=[]
        if(len(array_entrada)==len(array_saida)):
            for cont in range(0,len(array_entrada)-tamanho_entrada-tamanho_saida):
                if(array_entrada!=None):
                    linha = []
                    for array in array_entrada[cont:cont + tamanho_entrada]:
                        for valor in array:
                            linha.append(valor)
                    trainX.append(linha)
                if(array_saida!=None):
                    trainY.append([valor for valor in array_saida[cont+tamanho_entrada:cont+tamanho_entrada+tamanho_saida]])
            return trainX,trainY
    except Exception as e:
        tratamento_excessao("Erro")

def criar_modelo(tuple_camada_central,**kwargs):
    try:
        model=MLPRegressor(hidden_layer_sizes=tuple_camada_central,**kwargs)
        return model

    except Exception as e:
        tratamento_excessao("Erro")

def predict(model,array_entrada,quantidade_previsoes,tamanho_entrada):
    try:
        array_previsoes=[]
        while(len(array_previsoes)<quantidade_previsoes):
            array_previsao=numpy.array([array_entrada[-tamanho_entrada:]])
            previsao=model.predict(array_previsao)
            [array_entrada.append(valor) for valor in previsao[0]]
            [array_previsoes.append(valor) for valor in previsao[0]]
        return array_previsoes[:quantidade_previsoes]
    except infoerroexception as e:
        tratamento_excessao("Info")
    except Exception as e:
        tratamento_excessao("Erro")

def save_model(model,url_file):
    try:
        pickle.dump(model, open(url_file, 'wb'))
    except Exception as e:
        tratamento_excessao("Erro")

def load_model(url_file):
    try:
        model=pickle.load(open(url_file, 'rb'))
        return model
    except Exception as e:
        tratamento_excessao("Erro")


def fit(array_series_treinamento,array_serie_previsao,array_camadas,comprimento_sozonal,comprimento_saida):
    try:

        comprimento_sozonal=comprimento_sozonal*len(array_series_treinamento)
        array_series_treinamento.append(array_serie_previsao)
        arrays_mesmo_tamanho=estatisticas.Dimencionar_arrays(array_series_treinamento)
        array_treinamento=arrays_mesmo_tamanho[:-1]
        array_previsao=arrays_mesmo_tamanho[-1]
        array_treinamento=estatisticas.Agrupar_arrays(array_treinamento)
        TrainX,TrainY=criar_treinamento(array_treinamento,array_previsao,comprimento_sozonal,comprimento_saida)

        model=criar_modelo(tuple((array_camadas)),activation='relu', solver='adam', alpha=0.001, batch_size='auto',
                            learning_rate='adaptive', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True,
                            random_state=9, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
                            early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

        model.fit(TrainX,TrainY)

        return model

    except Exception as e:
        tratamento_excessao("Erro")

