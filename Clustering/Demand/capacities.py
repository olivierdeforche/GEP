import pandas as pd

xls_capacity = pd.DataFrame()

xls_capacity = pd.ExcelFile(f"C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/xls_capacity.xlsx", engine = 'openpyxl')

df_line = pd.read_excel(xls_capacity, 'Line')
filtered_2030 = df_line[df_line['Year'] == 2030]
filtered_CY = filtered_2030[filtered_2030['Climate Year'] == 2009]
filtered_DE = filtered_CY[filtered_CY['Scenario'] == 'Distributed Energy']
filtered_export = filtered_DE[filtered_DE['Parameter'] == 'Export Capacity (MW)']
filtered_import = filtered_DE[filtered_DE['Parameter'] == 'Import Capacity (MW)']
selected_export = filtered_export.loc[:, ['Node/Line', 'Value']]
selected_import = filtered_import.loc[:, ['Node/Line', 'Value']]

selected_export.to_csv(f"C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/export_capacity.csv")
selected_import.to_csv(f"C:/Users/Louis/Documents/Master/Thesis/GEP/GEP/import_capacity.csv")
