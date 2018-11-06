import pickle
from sklearn.linear_model import LinearRegression

from .. import estatisticas

def predict(model_fit,array):
    try:
        return model_fit.predict(array)
    except Exception as e:
        print(str(e))

def fit_model(train_array,prev_array,**kwargs):
    try:
        train_array.append(prev_array)
        array_dimencionado=estatisticas.Dimencionar_arrays(train_array)
        prev_array=array_dimencionado[-1]
        train_array=estatisticas.inverter_shape_array_2d(array_dimencionado[:-1])
        model=LinearRegression()
        model_fit=model.fit(train_array,prev_array)
        return model_fit
    except Exception as e:
        print(str(e))

def get_propriedades_modelo(model_fit):
    pass


def save_model(model,url_file):
    try:
        pickle.dump(model, open(url_file, 'wb'))
    except Exception as e:
        print(str(e))

def load_model(url_file):
    try:
        model=pickle.load(open(url_file, 'rb'))
        return model
    except Exception as e:
        print(str(e))
