import pickle
import statsmodels.api as sm

from ..estatisticas import Dimencionar_arrays

def predict(model_fit,array):
    try:
        return model_fit.predict(array)
    except Exception as e:
        print(str(e))

def fit_model(train_array,prev_array,**kwargs):
    array_dimencionado=Dimencionar_arrays(train_array.append(prev_array))
    train_array=array_dimencionado[:-1]
    prev_array=array_dimencionado[-1]
    model=sm.OLS(prev_array,train_array,**kwargs)
    model_fit=model.fit()

    return model_fit

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
