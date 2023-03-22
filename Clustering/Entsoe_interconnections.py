from entsoe import EntsoePandasClient, EntsoeRawClient
import pandas as pd

import netCDF4 as nc
import libpysal
import numpy as np
import matplotlib.pyplot as plt
import warnings
import time
import unittest
import csv
from scipy import interpolate
import itertools

# Initialize client
raw_client = EntsoeRawClient(api_key='1af97731-50b1-4166-acbf-8f9af34dc032')
client = EntsoePandasClient(api_key='1af97731-50b1-4166-acbf-8f9af34dc032')
# API KEY : <1af97731-50b1-4166-acbf-8f9af34dc032> DO NOT REMOVE
# https://github.com/EnergieID/entsoe-py/blob/master/README.md

# Define start and end dates
start = pd.Timestamp('2017-01-01', tz='Europe/Brussels')
end = pd.Timestamp('2018-01-01', tz='Europe/Brussels')
res = 8760

# ORIGINAL_NEIGHBOURS = {
#     'BE': ['NL', 'DE_AT_LU', 'FR', 'GB', 'DE_LU'],
#     'NL': ['BE', 'DE_AT_LU', 'DE_LU', 'GB', 'NO_2', 'DK_1'],
#     'DE_AT_LU': ['BE', 'CH', 'CZ', 'DK_1', 'DK_2', 'FR', 'IT_NORD', 'IT_NORD_AT', 'NL', 'PL', 'SE_4', 'SI'],
#     'FR': ['BE', 'CH', 'DE_AT_LU', 'DE_LU', 'ES', 'GB', 'IT_NORD', 'IT_NORD_FR'],
#     'CH': ['AT', 'DE_AT_LU', 'DE_LU', 'FR', 'IT_NORD', 'IT_NORD_CH'],
#     'AT': ['CH', 'CZ', 'DE_LU', 'HU', 'IT_NORD', 'SI'],
#     'CZ': ['AT', 'DE_AT_LU', 'DE_LU', 'PL', 'SK'],
#     'GB': ['BE', 'FR', 'IE_SEM', 'NL'],
#     'NO_2': ['DE_LU', 'DK_1', 'NL', 'NO_1', 'NO_5'],
#     'HU': ['AT', 'HR', 'RO', 'RS', 'SK', 'UA'],
#     'IT_NORD': ['CH', 'DE_AT_LU', 'FR', 'SI', 'AT', 'IT_CNOR'],
#     'ES': ['FR', 'PT'],
#     'SI': ['AT', 'DE_AT_LU', 'HR', 'IT_NORD'],
#     'RS': ['AL', 'BA', 'BG', 'HR', 'HU', 'ME', 'MK', 'RO'],
#     'PL': ['CZ', 'DE_AT_LU', 'DE_LU', 'LT', 'SE_4', 'SK', 'UA'],
#     'ME': ['AL', 'BA', 'RS'],
#     'DK_1': ['DE_AT_LU', 'DE_LU', 'DK_2', 'NO_2', 'SE_3', 'NL'],
#     'RO': ['BG', 'HU', 'RS', 'UA'],
#     'LT': ['BY', 'LV', 'PL', 'RU_KGD', 'SE_4'],
#     'BG': ['GR', 'MK', 'RO', 'RS', 'TR'],
#     'SE_3': ['DK_1', 'FI', 'NO_1', 'SE_2', 'SE_4'],
#     'LV': ['EE', 'LT', 'RU'],
#     'IE_SEM': ['GB'],
#     'BA': ['HR', 'ME', 'RS'],
#     'NO_1': ['NO_2', 'NO_3', 'NO_5', 'SE_3'],
#     'SE_4': ['DE_AT_LU', 'DE_LU', 'DK_2', 'LT', 'PL'],
#     'NO_5': ['NO_1', 'NO_2', 'NO_3'],
#     'SK': ['CZ', 'HU', 'PL', 'UA'],
#     'EE': ['FI', 'LV', 'RU'],
#     'DK_2': ['DE_AT_LU', 'DE_LU', 'DK_1', 'SE_4'],
#     'FI': ['EE', 'NO_4', 'RU', 'SE_1', 'SE_3'],
#     'NO_4': ['SE_2', 'FI', 'NO_3', 'SE_1'],
#     'SE_1': ['FI', 'NO_4', 'SE_2'],
#     'SE_2': ['NO_3', 'NO_4', 'SE_1', 'SE_3'],
#     'DE_LU': ['AT', 'BE', 'CH', 'CZ', 'DK_1', 'DK_2', 'FR', 'NO_2', 'NL', 'PL', 'SE_4'],
#     'MK': ['BG', 'GR', 'RS'],
#     'PT': ['ES'],
#     'GR': ['AL', 'BG', 'IT_BRNN', 'IT_GR', 'MK', 'TR'],
#     'NO_3': ['NO_1', 'NO_4', 'NO_5', 'SE_2'],
#     'IT': ['AT', 'FR', 'GR', 'MT', 'ME', 'SI', 'CH'],
#     'IT_BRNN': ['GR', 'IT_SUD'],
#     'IT_SUD': ['IT_BRNN', 'IT_CSUD', 'IT_FOGN', 'IT_ROSN', 'IT_CALA'],
#     'IT_FOGN': ['IT_SUD'],
#     'IT_ROSN': ['IT_SICI', 'IT_SUD'],
#     'IT_CSUD': ['IT_CNOR', 'IT_SARD', 'IT_SUD'],
#     'IT_CNOR': ['IT_NORD', 'IT_CSUD', 'IT_SARD'],
#     'IT_SARD': ['IT_CNOR', 'IT_CSUD'],
#     'IT_SICI': ['IT_CALA', 'IT_ROSN', 'MT'],
#     'IT_CALA': ['IT_SICI', 'IT_SUD'],
#     'MT': ['IT_SICI'],
#     'HR': ['BA', 'HU', 'RS', 'SI']
# }

neighbours = {
    'BE': ['NL', 'FR'],
    'NL': ['BE', 'DE_AT_LU', 'GB', 'NO_2'],
    'DE_AT_LU': ['HU', 'CH', 'CZ', 'DK_1', 'DK_2', 'FR', 'IT_NORD_AT', 'NL', 'SE_4', 'SI'],
    'FR': ['BE', 'CH', 'DE_AT_LU', 'ES', 'GB'],
    'CH': ['DE_AT_LU', 'FR', 'IT_NORD'],
    'CZ': ['DE_AT_LU', 'PL', 'SK'],
    'GB': ['FR', 'NL'],
    'NO_1': ['NO_2', 'NO_3', 'NO_5', 'SE_3'],
    'NO_2': ['DK_1', 'NL', 'NO_1', 'NO_5'],
    'NO_3': ['NO_1', 'NO_4', 'NO_5', 'SE_2'],
    'NO_4': ['SE_2', 'NO_3', 'SE_1'],
    'NO_5': ['NO_1', 'NO_2', 'NO_3'],
    'HU': ['AT', 'HR', 'RO', 'RS', 'SK'],
    'ES': ['FR', 'PT'],
    'SI': ['AT', 'DE_AT_LU', 'HR', 'IT_NORD'],
    'RS': ['AL', 'BA', 'BG', 'HR', 'HU', 'ME', 'MK', 'RO'],
    'PL': ['CZ', 'LT', 'SE_4'],
    'ME': ['RS'],
    'DK_1': ['DE_AT_LU', 'DK_2', 'NO_2', 'SE_3'],
    'RO': ['BG', 'HU', 'RS'],
    'LT': ['BY', 'LV', 'PL', 'RU_KGD', 'SE_4'],
    'BG': ['GR', 'MK', 'RO', 'RS'],
    'SE_3': ['DK_1', 'FI', 'NO_1', 'SE_2', 'SE_4'],
    'LV': [ 'LT'],
    'BA': ['HR', 'RS'],
    'SE_4': ['DE_AT_LU', 'DK_2', 'LT', 'PL'],
    'SK': ['CZ', 'HU'],
    'EE': ['FI', 'RU'],
    'DK_2': ['DE_AT_LU','DK_1', 'SE_4'],
    'FI': ['EE', 'RU', 'SE_1', 'SE_3'],
    'SE_1': ['FI', 'NO_4', 'SE_2'],
    'SE_2': ['NO_3', 'NO_4', 'SE_1', 'SE_3'],
    'MK': ['BG', 'GR', 'RS'],
    'PT': ['ES'],
    'GR': ['AL', 'BG', 'IT', 'MK', 'TR'],
    'IT': ['AT', 'FR', 'GR', 'SI', 'CH'],
    'HR': ['BA', 'HU', 'RS', 'SI']
}

# #Load
# start_load = time.time()
# load = {}
#
# for key in neighbours:
#     print(key)
#     load[key] = []
#     ld = client.query_load(key, start=start, end=end)
#     ld = ld.values.tolist()
#     ld = list(np.concatenate(ld).flat)
#     #interpolate to desired length
#     f = interpolate.interp1d(np.arange(len(ld)), ld, kind='cubic')
#     new_indices = np.linspace(0, len(ld) - 1, res)
#     ld = f(new_indices)
#     ld = np.array(ld)
#     print(ld)
#     load[key].append(ld)
#
# print(load)
# end_load = time.time()
# print('Computational time load:')
# print((end_load-start_load)/3600, 'h')
#
# with open('load_europe.csv', 'w') as output:
#     writer = csv.writer(output)
#     for key in load:
#         for val in load[key]:
#             writer.writerow([key, *val])


#capacities
start_capacities = time.time()
capacities = {}

for key in neighbours:
    capacities[key] = []
    country_code_from = key
    for value in neighbours[key]:
        print(key)
        print(value)
        country_code_to = value
        trans = client.query_net_transfer_capacity_yearahead(country_code_from, country_code_to, start=start, end=end)
        trans = trans.values.tolist()
        print(trans)
        capacities[key].append(trans)

print(capacities)
end_capacities = time.time()
print('Computational time capacities:')
print((end_capacities-start_capacities)/3600)

with open("capacities_europe.csv", 'w') as f:
    w = csv.DictWriter(f, capacities.keys())
    w.writeheader()
    w.writerow(capacities)


# ts = client.query_import(country_code, start=start, end=end)
# ts.to_csv('import.csv')
#
# ts = client.query_day_ahead_prices(country_code, start=start, end=end)
# ts.to_csv('day_ahead_prices.csv')
#
# ts = client.query_crossborder_flows(country_code_from, country_code_to, start=start, end=end)
# ts.to_csv('crossborder_flows.csv')
#
# ts = client.query_load(country_code, start=start,end=end)
# ts.to_csv('load.csv')

# # methods that return Pandas Series
# client.query_day_ahead_prices(country_code, start=start, end=end)
# client.query_net_position(country_code, start=start, end=end, dayahead=True)
# client.query_crossborder_flows(country_code_from, country_code_to, start=start, end=end)
# client.query_scheduled_exchanges(country_code_from, country_code_to, start=start, end=end, dayahead=False)
# client.query_net_transfer_capacity_dayahead(country_code_from, country_code_to, start=start, end=end)
# client.query_net_transfer_capacity_weekahead(country_code_from, country_code_to, start=start, end=end)
# client.query_net_transfer_capacity_monthahead(country_code_from, country_code_to, start=start, end=end)
# client.query_net_transfer_capacity_yearahead(country_code_from, country_code_to, start=start, end=end)
# client.query_intraday_offered_capacity(country_code_from, country_code_to, start=start, end=end,implicit=True)
# client.query_offered_capacity(country_code_from, country_code_to,contract_marketagreement_type, start=start, end=end, implicit=True)
# client.query_aggregate_water_reservoirs_and_hydro_storage(country_code, start=start, end=end)
#
# # methods that return Pandas DataFrames
# client.query_load(country_code, start=start,end=end)
# client.query_load_forecast(country_code, start=start,end=end)
# client.query_load_and_forecast(country_code, start=start, end=end)
# client.query_generation_forecast(country_code, start=start,end=end)
# client.query_wind_and_solar_forecast(country_code, start=start,end=end, psr_type=None)
# client.query_generation(country_code, start=start,end=end, psr_type=None)
# client.query_generation_per_plant(country_code, start=start,end=end, psr_type=None)
# client.query_installed_generation_capacity(country_code, start=start,end=end, psr_type=None)
# client.query_installed_generation_capacity_per_unit(country_code, start=start,end=end, psr_type=None)
# client.query_imbalance_prices(country_code, start=start,end=end, psr_type=None)
# client.query_contracted_reserve_prices(country_code, type_marketagreement_type, start=start, end=end, psr_type=None)
# client.query_contracted_reserve_amount(country_code, type_marketagreement_type,  start=start, end=end, psr_type=None)
# client.query_unavailability_of_generation_units(country_code, start=start, end=end, docstatus=None, periodstartupdate=None, periodendupdate=None)
# client.query_unavailability_of_production_units(country_code, start=start, end=end, docstatus=None, periodstartupdate=None, periodendupdate=None)
# client.query_unavailability_transmission(country_code_from, country_code_to, start=start, end=end, docstatus=None, periodstartupdate=None, periodendupdate=None)
# client.query_withdrawn_unavailability_of_generation_units(country_code, start=start, end=end)
# client.query_import(country_code, start=start,end=end)
# client.query_generation_import(country_code, start=start,end=end)
# client.query_procured_balancing_capacity(country_code, process_type, start=start,end=end, type_marketagreement_type=None)

