from NEAT_pipeline import start_pipeline
import pandas as pd

api_key = 'XlcQuHE1hrCzNEfej695gyAGREGQIhL4lRurJqgJFv32nhP9fTpdtUJOr5cQEqBV'

addresses = []

with open('/Users/matthewschultz/Big_Data_Lab/identity_review/current_scripts/list.txt') as f:
    for line in f:
        addresses.append(line.rstrip().lower())

final = []

for address in addresses:
    temp = start_pipeline(api_key, address)
    final.append(temp)

final = pd.concat(final, ignore_index=True)

final.to_csv('/Users/matthewschultz/Big_Data_Lab/identity_review/csv_output/test_data.csv', index=None)


