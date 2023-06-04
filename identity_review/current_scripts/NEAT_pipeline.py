# import packages 
import sys
import pandas as pd
from NEAT_get_transaction import get_transaction_history
import pickle
import os
import numpy as np
import sklearn

# get most updated random forest model
def _get_current_rf(path):
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

def _get_num_malcious_accounts(current_history, model, scalar):
    to_be_normalized = scalar.transform(current_history[['value', 'time_b/w_trans']])

    not_normalized = current_history[['day', 'hour', 'type_of_trans']].to_numpy()

    combined = np.concatenate((to_be_normalized, not_normalized), axis = 1)

    normalized = pd.DataFrame(combined)
    normalized = normalized.rename(columns = {
        0: 'value',
        1: 'time_b/w_trans',
        2: 'day',
        3: 'hour',
        4: 'type_of_trans',
    })
    predicted = []
    for index, row in normalized.iterrows():
        predict = model.predict(row[['value', 'time_b/w_trans', 'day', 'hour','type_of_trans']].to_numpy().reshape(1, -1))
        predicted.append(predict)

    normalized["malicious"] = predicted

    num_of_mal_trans = len(normalized.loc[normalized['malicious'] == 1])
    return num_of_mal_trans

def _get_ratio_in_out(current_history):
    value_out = current_history.loc[current_history['type_of_trans'] == 1]
    value_out = sum(value_out['value'])
    value_in = current_history.loc[current_history['type_of_trans'] == 0]
    value_in = sum(value_in['value'])
    if value_in < 1:
        value_in = 1
    ratio = value_out / value_in
    return value_out, value_in, ratio

def _get_avg_trans_per_day(df):
    months = [*set(df['month'])]
    days = [*set(df['day'])]
    df['block_timestamp'].astype('str')
    try:
        day_by_day = [len(df.loc[df['block_timestamp'].str.contains('{}-{}'.format(month, day), case=False, na=False)]) for month in months for day in days]
        day_by_day = [val for val in day_by_day if val > 0]
        return sum(day_by_day) / len(day_by_day)
    except:
        day_by_day = [len(df.loc[df['block_timestamp'].str.contains(r'(?:(?:(-?(0){}|-{}))-(?:(-?(0){}|-{})))'.format(month, month, day, day), case=False, na=False)]) for month in months for day in days]
        day_by_day = [val for val in day_by_day if val > 0]
        if len(day_by_day) == 0:
            return 1
        else:
            return sum(day_by_day) / len(day_by_day)

def start_pipeline(api_key, address):
    try:
        current_history = get_transaction_history(api_key, address)
        path = "identity_review/iteration_rand_forest/"
        model = _get_current_rf(path)
        scalar = _get_current_normalizer("identity_review/normalizer/")
        _num_of_mal_trans = _get_num_malcious_accounts(current_history, model, scalar)
        _val_out, _val_in, _ratio = _get_ratio_in_out(current_history)
        _avg_trans = _get_avg_trans_per_day(current_history)
        _num_of_zero = len(current_history.loc[current_history['time_b/w_trans'] == 0])
        neat_df = pd.DataFrame({'address': [address],
                                'num_of_mal_trans': [_num_of_mal_trans],
                                'ratio': [_ratio],
                                'value_out': [_val_out],
                                'value_in': [_val_in],
                                'avg_trans': [_avg_trans],
                                'num_of_zero': [_num_of_zero]})
        return neat_df
    except:
        print("an error has occured")
        neat_df = pd.DataFrame({'address': [address],
            'num_of_mal_trans': [-1],
            'ratio': [-1],
            'value_out': [-1],
            'value_in': [-1],
            'avg_trans': [-1],
            'num_of_zero': [-1]})

        return neat_df






