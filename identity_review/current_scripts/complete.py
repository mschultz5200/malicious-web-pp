import pandas as pd
import pickle
import os
from NEAT_pipeline import start_pipeline
import numpy as np

# mlp created in the mlp jupyter notebook
def _get_current_mlp(path):
    try:
        list_files = os.listdir(path)
        files = [file for file in list_files if file != '.DS_Store']
        files.sort()
        model = pickle.load(open(path + files[-1], 'rb'))
        return model
    except FileNotFoundError as fe:
        print(str(fe) + "\nReturning Object of Class None.")
        return None
    except pickle.UnpicklingError as pe:
        print("Error when unpickling file: " + str(pe) + ".\nReturning Object of Class None.")
        return None

# normalizer created in mlp jupyter notebook
def _get_current_normalizer(path):
    try:
        list_files = os.listdir(path)
        files = [file for file in list_files if file != '.DS_Store']
        files.sort()
        model = pickle.load(open(path + files[-1], 'rb'))
        return model
    except FileNotFoundError as fe:
        print(str(fe) + "\nReturning Object of Class None.")
        return None
    except pickle.UnpicklingError as pe:
        print("Error when unpickling file: " + str(pe) + ".\nReturning Object of Class None.")
        return None
    

def normalize(df, normalizer):
    scaled = normalizer.transform(df[['num_of_mal_trans', 'ratio']])
    temp = df[['value_out', 'value_out', 'avg_trans', 'num_of_zero', ]].to_numpy()

    combined = np.concatenate((scaled, temp), axis = 1)

    normalized = pd.DataFrame(combined)
    normalized = normalized.rename(columns = {
        0: 'num_of_mal_trans',
        1: 'ratio',
        2: 'value_out',
        3: 'value_in',
        4: 'avg_trans',
        5: 'num_of_zero',
    })

    return normalized

def predict(address, model):
    input = address[['num_of_mal_trans', 'ratio', 'value_out', 'value_in', 'avg_trans', 'num_of_zero']].to_numpy().reshape(1,-1)
    predicted = []
    predicted.append(model.predict(input))
    address['output'] = predicted
    return address

def predict_malicious(api_key, address):
    tested_address = start_pipeline(api_key, address)
    path_mlp = "identity_review/mlp_iteration/"
    model = _get_current_mlp(path_mlp)
    path_scalar = 'identity_review/mlp_normalizer/'
    scalar = _get_current_normalizer(path_scalar)
    normalized = normalize(tested_address, scalar)
    output = predict(normalized, model)
    return output


# 0x1954829e72A0477fa146423ee09E9bEF340c80f5
# 0xb8D76f4BC2518F8eb508bf0Ccca76f8F9DD57a3f