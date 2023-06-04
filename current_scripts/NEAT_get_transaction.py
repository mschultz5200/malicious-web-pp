import time
from datetime import datetime
import regex as re
import pandas as pd
from moralis import evm_api
import json
import string

def _clean_time(time):
    split_time = re.split(r"T", time)
    date = split_time[0]
    time = re.split(r".000Z", split_time[1])
    d_t = date + " " + time[0]
    return d_t

# Function to convert string to datetime
def _convert(date_time):
    cleaned_time = _clean_time(date_time)
    format = '%Y-%m-%d %H:%M:%S'  # The format
    datetime_str = datetime.strptime(cleaned_time, format)
    return datetime_str

def _get_elapsed_time(df):
    time_elapsed = []
    day = []
    month = []
    hour = []
    for index, row in df.iterrows():
        if index == 0: 
            time_elapsed.append(0)
            day.append(_convert(row['block_timestamp']).day)
            month.append(_convert(row['block_timestamp']).month)
            hour.append(_convert(row['block_timestamp']).hour)
        else:
            temp = _convert(df.iloc[index]['block_timestamp']) - _convert(df.iloc[index - 1]['block_timestamp'])
            final = int(temp.total_seconds())
            time_elapsed.append(final)
            day.append(_convert(row['block_timestamp']).day)
            month.append(_convert(row['block_timestamp']).month)
            hour.append(_convert(row['block_timestamp']).hour)
    return time_elapsed, day, month, hour
   

def _create_data_frame(results, address):

    results['value'] = results['value'].div(10 ** 18)

    new_df = results[['to_address', 'from_address', 'value', 'gas', 'block_timestamp']]

    new_df = new_df.loc[::-1].reset_index()

    time_between, hour, month, day = _get_elapsed_time(new_df)
    new_df['time_b/w_trans'] = time_between
    new_df['day'] = day
    new_df['month'] = month
    new_df['hour'] = hour

    type_of_trans = []
    for index, row in new_df.iterrows():
        if row['to_address'] == address.lower():
            type_of_trans.append(0)
        else:
            type_of_trans.append(1)
    
    new_df['type_of_trans'] = type_of_trans
    return new_df


def _call_api(api_key, address, cursor):
    if cursor == '':
        params = {
            "address": address, 
            "chain": "eth",
        }
    else: 
        params = {
            "address": address, 
            "chain": "eth",
            'cursor': cursor,
        }

    result = evm_api.transaction.get_wallet_transactions(
        api_key=api_key,
        params=params,
    )
    final_json = json.dumps(result['result'], indent=4, sort_keys=True)

    temp_df = pd.read_json(final_json)
    previous_cursor = result['cursor']

    return temp_df, previous_cursor


def get_transaction_history(api_key, address):
    list_of_histories = []
    previous_cursor = ""
    nextCursor = True
    index = 0
    
    while nextCursor:
        print(index)
        if previous_cursor == "":
           
           temp, previous_cursor = _call_api(api_key, address, previous_cursor)
           list_of_histories.append(temp)

           if previous_cursor == None:
               nextCursor = False
        else:
            temp, previous_cursor = _call_api(api_key, address, previous_cursor)
            list_of_histories.append(temp)

            if previous_cursor == None:
                nextCursor = False
        
        index = index + 1

    df = _create_data_frame(pd.concat(list_of_histories, ignore_index=True), address)
    return df
    




