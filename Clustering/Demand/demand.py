import pandas as pd

scenario = "NationalTrends"
year = 2030
CY = 2013
df_demand = pd.DataFrame()

# xls_dem = pd.ExcelFile( f"../Input Data/Demand_time_series/Demand_TimeSeries_{year}_{scenario}.xlsx",engine = 'openpyxl')
xls_dem = pd.ExcelFile(f"C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Demand kristof/Demand_TimeSeries_{year}_{scenario}.xlsx", engine = 'openpyxl')

counter = 0
for sheet_name in xls_dem.sheet_names:
    print(counter)
    df_sheet = pd.read_excel(xls_dem, sheet_name)
    row_number = df_sheet[df_sheet.iloc[:, 0] == "Date"].first_valid_index()
    date_row = df_sheet.iloc[row_number].reset_index(drop = True)
    col_index_for_CY = date_row[date_row == CY].first_valid_index()
    df_demand[sheet_name] = df_sheet.iloc[row_number+1:row_number+8761,col_index_for_CY]
    counter += 1

# df_demand.to_csv(f"../Input Data/time_series_output/Demand_{year}_{scenario}_{CY}.csv")
df_demand.to_csv(f"C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Demand kristof/Demand_TimeSeries_output_{year}_{scenario}_{str(CY)}.csv")
