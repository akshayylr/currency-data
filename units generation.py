# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 18:19:32 2023

@author: aksha
"""

import csv

# Function to extract first three letters from odd rows and last three from even rows
def extract_letters(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        odd_first_three = set()
        even_last_three = set()

        for i, row in enumerate(reader, start=1):
            fx_name = row['FX_Name']
            if i % 2 != 0:  # Odd rows
                if fx_name != 'USD':
                    odd_first_three.add(fx_name[:3])
            else:  # Even rows
                if fx_name != 'USD':
                    even_last_three.add(fx_name[-3:])
    
    return odd_first_three, even_last_three

file_path = 'C:/Users/aksha/Downloads/data_eng_fin/profit and loss/Trading_Schedule.csv'

# Extract letters from FX_Name column in odd and even rows excluding 'USD'
odd_first_three, even_last_three = extract_letters(file_path)

# Merge unique values from both sets into a single list
merged_unique_list = list(odd_first_three | even_last_three)

# Print the merged unique list
print("Merged unique list of first three and last three letters (excluding 'USD'):")
print(merged_unique_list)


from polygon import RESTClient
client = RESTClient("beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq");
currency_values = {}
# Iterate through each unique currency and fetch real-time conversion rates
for currency in merged_unique_list:
    if currency != 'USD':  # Skip USD as it's the base currency
        res = client.get_real_time_currency_conversion("USD", currency, precision=5)
        currency_values[currency] = res.converted

print("Currency Values Dictionary:")
print(currency_values)


import pandas as pd

# Function to calculate contract equivalents
def calculate_contracts(currency_pair, direction, units=100):
    if direction == 1:
        last_three_letters = currency_pair[-3:]
        if last_three_letters in currency_values:
            currency_value = currency_values[last_three_letters]
            contracts = 100 * round(currency_value, 2)
            print(last_three_letters,contracts)
            # with open('CURRENCY.txt', 'a') as f:
            #     f.write('%s\n' % last_three_letters)
            return round(contracts)
        
        else:
            return 100
    elif direction == -1:
        first_three_letters = currency_pair[:3]
        if first_three_letters in currency_values:
            currency_value = currency_values[first_three_letters]
            contracts = 100 * round(currency_value, 2)
            print(first_three_letters,contracts)
            return round(contracts)
        else:
            return 100

    return None

# Function to update Trading_Schedule.csv and save as a new file
def save_new_file_with_contracts(input_file_path, output_file_path):
    # Load the Trading_Schedule.csv file
    schedule_df = pd.read_csv(input_file_path)

    # Create a new column 'Contract_Equivalents' based on direction and currency values
    schedule_df['Units'] = schedule_df.apply(lambda row: calculate_contracts(row['FX_Name'], row['Direction'], row['Units']), axis=1)

    # Save the updated DataFrame to a new file
    schedule_df.to_csv(output_file_path, index=False)
output_file_path = 'C:/Users/aksha/Downloads/data_eng_fin/profit and loss/simulator/Trading_Schedule_Converted.csv'
# Update the Trading_Schedule.csv file with contract equivalents and save as a new file
save_new_file_with_contracts(file_path, output_file_path)
