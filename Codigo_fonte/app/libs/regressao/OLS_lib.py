import pickle
import statsmodels.api as sm

from ..estatisticas import Dimencionar_arrays,inverter_shape_array_2d

def predict(model_fit,array):
    try:
        return model_fit.predict(array)
    except Exception as e:
        print(str(e))

def fit_model(train_array,prev_array,**kwargs):
    try:
        train_array.append(prev_array)
        print(len(train_array))
        array_dimencionado=Dimencionar_arrays(train_array)
        prev_array=array_dimencionado[-1]
        train_array=inverter_shape_array_2d(array_dimencionado[:-1])
        model=sm.OLS(prev_array,train_array)
        model_fit=model.fit()

        return model_fit
    except Exception as e:
        print(str(e))

def get_propriedades_modelo(model_fit):
    dict_propriedades={
        "aic":model_fit.aic,
        "bic":model_fit.bic,
        "bse":model_fit.bse,
        "r quadrado":model_fit.rsquared,
        "mse modelo":model_fit.mse_model,
        "mse residos":model_fit.mse_resid,
        "mse total":model_fit.mse_total,
        "resido":model_fit.resid,
        "parametros":model_fit.params
    }

    return dict_propriedades

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
