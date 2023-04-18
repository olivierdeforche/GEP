import pandas as pd

scenario = "NationalTrends"
year = 2030
CY = 2013
df_demand = pd.DataFrame()

# xls_dem = pd.ExcelFile( f"../Input Data/Demand_time_series/Demand_TimeSeries_{year}_{scenario}.xlsx",engine = 'openpyxl')
xls_dem = pd.ExcelFile(f"C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Demand/Demand_TimeSeries_{year}_{scenario}.xlsx", engine = 'openpyxl')

counter = 0
for sheet_name in xls_dem.sheet_names:
    print(counter)
    df_sheet = pd.read_excel(xls_dem, sheet_name)
    row_number = df_sheet[df_sheet.iloc[:, 0] == "Date"].first_valid_index()
    date_row = df_sheet.iloc[row_number].reset_index(drop = True)
    col_index_for_CY = date_row[date_row == CY].first_valid_index()
    df_demand[sheet_name] = df_sheet.iloc[row_number+1:row_number+8761,col_index_for_CY]
    counter += 1

df_demand.columns = [col.replace('0', '') for col in df_demand.columns]
df_demand = df_demand.rename(columns={'ITCN': 'IT'})
cols_to_sum = ['IT', 'ITCS', 'ITN1', 'ITS1', 'ITSA', 'ITSI']
df_demand['IT'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['ITCS', 'ITN1', 'ITS1', 'ITSA', 'ITSI']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

df_demand = df_demand.rename(columns={'DKE1': 'DK'})
cols_to_sum = ['DK', 'DKW1']
df_demand['DK'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['DKW1']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

cols_to_sum = ['FR', 'FR15']
df_demand['FR'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['FR15']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

cols_to_sum = ['GR', 'GR3']
df_demand['GR'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['GR3']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

df_demand = df_demand.rename(columns={'NOS': 'NO'})
cols_to_sum = ['NO', 'NON1', 'NOM1']
df_demand['NO'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['NON1', 'NOM1']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

df_demand = df_demand.rename(columns={'SE1': 'SE'})
cols_to_sum = ['SE', 'SE2', 'SE3', 'SE4']
df_demand['SE'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['SE2', 'SE3', 'SE4']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

df_demand = df_demand.rename(columns={'LUB1': 'LU'})
cols_to_sum = ['LU', 'LUF1', 'LUG1']
df_demand['LU'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['LUF1', 'LUG1']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

cols_to_sum = ['UK', 'UKNI']
df_demand['UK'] = df_demand[cols_to_sum].sum(axis=1)
cols_to_sum = ['UKNI']
df_demand.drop(cols_to_sum, axis=1, inplace=True)

# df_demand.to_csv(f"../Input Data/time_series_output/Demand_{year}_{scenario}_{CY}.csv")
df_demand.to_csv(f"C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Demand/Demand_TimeSeries_output_{year}_{scenario}_{str(CY)}.csv",index=False)
