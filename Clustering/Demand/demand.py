import pandas as pd

scenario = "NationalTrends"
year = 2030
CY = 2013
df_demand = pd.DataFrame()

# xls_dem = pd.ExcelFile( f"../Input Data/Demand_time_series/Demand_TimeSeries_{year}_{scenario}.xlsx",engine = 'openpyxl')
xls_dem = pd.ExcelFile(f"C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/Demand_TimeSeries_{year}_{scenario}.xlsx", engine = 'openpyxl')

counter = 0
for sheet_name in xls_dem.sheet_names:
    print(counter)
    df_sheet = pd.read_excel(xls_dem, sheet_name)
    row_number = df_sheet[df_sheet.iloc[:, 0] == "Date"].first_valid_index()
    date_row = df_sheet.iloc[row_number].reset_index(drop = True)
    col_index_for_CY = date_row[date_row == CY].first_valid_index()
    df_demand[sheet_name] = df_sheet.iloc[row_number+1:row_number+8761,col_index_for_CY]
    counter += 1

# Remove 0 from column names
df_demand.columns = [col.replace('0', '') for col in df_demand.columns]

# Rename the column
df_demand.rename(columns={'DKE1': 'DK', 'SE1': 'SE', 'ITCN':'IT','LUB1':'LU','NOM1':'NO','UA1':'UA'}, inplace=True)

## Sum columns
# Denmark
df_demand['DK'] = df_demand['DK'] + df_demand['DKW1']
df_demand.drop('DKW1', axis=1, inplace=True)

# France
df_demand['FR'] = df_demand['FR'] + df_demand['FR15']
df_demand.drop('FR15', axis=1, inplace=True)

# Greece
df_demand['GR'] = df_demand['GR'] + df_demand['GR3']
df_demand.drop('GR3', axis=1, inplace=True)

# Italy
df_demand['IT'] = df_demand['IT'] + df_demand['ITCS'] + df_demand['ITN1'] + df_demand['ITS1'] + df_demand['ITSA'] + df_demand['ITSI']
df_demand.drop('ITCS', axis=1, inplace=True)
df_demand.drop('ITN1', axis=1, inplace=True)
df_demand.drop('ITS1', axis=1, inplace=True)
df_demand.drop('ITSA', axis=1, inplace=True)
df_demand.drop('ITSI', axis=1, inplace=True)

# Luxembourg
df_demand['LU'] = df_demand['LU'] + df_demand['LUF1'] + df_demand['LUG1']
df_demand.drop('LUF1', axis=1, inplace=True)
df_demand.drop('LUG1', axis=1, inplace=True)

# Sweden
df_demand['SE'] = df_demand['SE'] + df_demand['SE2'] + df_demand['SE3'] + df_demand['SE4']
df_demand.drop('SE2', axis=1, inplace=True)
df_demand.drop('SE3', axis=1, inplace=True)
df_demand.drop('SE4', axis=1, inplace=True)

# Norway
df_demand['NO'] = df_demand['NO'] + df_demand['NON1'] + df_demand['NOS']
df_demand.drop('NON1', axis=1, inplace=True)
df_demand.drop('NOS', axis=1, inplace=True)

# UK
df_demand['UK'] = df_demand['UK'] + df_demand['UKNI']
df_demand.drop('UKNI', axis=1, inplace=True)


# df_demand.to_csv(f"../Input Data/time_series_output/Demand_{year}_{scenario}_{CY}.csv")
df_demand.to_csv(f"C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Demand/Demand_TimeSeries_output_{year}_{scenario}_{str(CY)}.newformat.csv")
