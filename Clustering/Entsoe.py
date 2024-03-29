from entsoe import EntsoePandasClient
import pandas as pd

import netCDF4 as nc
import libpysal
import numpy as np
import matplotlib.pyplot as plt
import warnings
import time
import unittest

# Initialize client
client = EntsoePandasClient(api_key='1af97731-50b1-4166-acbf-8f9af34dc032')
# API KEY : <1af97731-50b1-4166-acbf-8f9af34dc032> DO NOT REMOVE
# https://github.com/EnergieID/entsoe-py/blob/master/README.md

# Define start and end dates
start = pd.Timestamp('2017-12-01', tz='Europe/Brussels')
end = pd.Timestamp('2018-01-01', tz='Europe/Brussels')

# Get available countries
countries = client.query_available_countries()
country_code = 'BE'  # Belgium
country_code_from = 'FR'  # France
country_code_to = 'DE' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"


# from utils import load_zones
# import plotly.express as px
# import pandas as pd
#
# zones = ['some', 'ISO2', 'codes']
#
# geo_df = load_zones(zones, pd.Timestamp(start_time))
# geo_df['value'] = range(1,len(geo_df)+1)
#
# fig = px.choropleth(geo_df,
#                    geojson=geo_df.geometry,
#                    locations=geo_df.index,
#                    color="value",
#                    projection="mercator",
#                    color_continuous_scale='rainbow')
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()

ts = client.query_import(country_code, start=start, end=end)
ts.to_csv('import.csv')

ts = client.query_day_ahead_prices(country_code, start=start, end=end)
ts.to_csv('day_ahead_prices.csv')

ts = client.query_crossborder_flows(country_code_from, country_code_to, start=start, end=end)
ts.to_csv('crossborder_flows.csv')

# methods that return Pandas Series
print(client.query_day_ahead_prices(country_code, start=start, end=end))
client.query_net_position(country_code, start=start, end=end, dayahead=True)
client.query_crossborder_flows(country_code_from, country_code_to, start=start, end=end)
client.query_scheduled_exchanges(country_code_from, country_code_to, start=start, end=end, dayahead=False)
# client.query_net_transfer_capacity_dayahead(country_code_from, country_code_to, start=start, end=end)
# client.query_net_transfer_capacity_weekahead(country_code_from, country_code_to, start=start, end=end)
# client.query_net_transfer_capacity_monthahead(country_code_from, country_code_to, start=start, end=end)
# client.query_net_transfer_capacity_yearahead(country_code_from, country_code_to, start=start, end=end)
# client.query_intraday_offered_capacity(country_code_from, country_code_to, start=start, end=end,implicit=True)
# client.query_offered_capacity(country_code_from, country_code_to,contract_marketagreement_type, start=start, end=end, implicit=True)
# client.query_aggregate_water_reservoirs_and_hydro_storage(country_code, start=start, end=end)

# methods that return Pandas DataFrames
client.query_load(country_code, start=start,end=end)
client.query_load_forecast(country_code, start=start,end=end)
client.query_load_and_forecast(country_code, start=start, end=end)
client.query_generation_forecast(country_code, start=start,end=end)
client.query_wind_and_solar_forecast(country_code, start=start,end=end, psr_type=None)
client.query_generation(country_code, start=start,end=end, psr_type=None)
client.query_generation_per_plant(country_code, start=start,end=end, psr_type=None)
client.query_installed_generation_capacity(country_code, start=start,end=end, psr_type=None)
client.query_installed_generation_capacity_per_unit(country_code, start=start,end=end, psr_type=None)
client.query_imbalance_prices(country_code, start=start,end=end, psr_type=None)
# client.query_contracted_reserve_prices(country_code, start, end, type_marketagreement_type, psr_type=None)
# client.query_contracted_reserve_amount(country_code, start, end, type_marketagreement_type, psr_type=None)
client.query_unavailability_of_generation_units(country_code, start=start,end=end, docstatus=None, periodstartupdate=None, periodendupdate=None)
client.query_unavailability_of_production_units(country_code, start, end, docstatus=None, periodstartupdate=None, periodendupdate=None)
client.query_unavailability_transmission(country_code_from, country_code_to, start, end, docstatus=None, periodstartupdate=None, periodendupdate=None)
client.query_withdrawn_unavailability_of_generation_units(country_code, start, end)
client.query_import(country_code, start, end)
client.query_generation_import(country_code, start, end)
client.query_procured_balancing_capacity(country_code, start, end, process_type, type_marketagreement_type=None)

