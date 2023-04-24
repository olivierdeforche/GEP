import pandas as pd
import numpy as np

xls_capacity = pd.DataFrame()

xls_capacity = pd.ExcelFile(f"C:/Users/Louis/iCloudDrive/Documents/Master/Thesis/DATA/xls_capacity.xlsx", engine = 'openpyxl')

# Filter necessary information from xls file
df_line = pd.read_excel(xls_capacity, 'Line')
filtered_2030 = df_line[df_line['Year'] == 2030]
filtered_CY = filtered_2030[filtered_2030['Climate Year'] == 2009]
filtered_DE = filtered_CY[filtered_CY['Scenario'] == 'Distributed Energy']
filtered_DE = filtered_DE.copy()

# Rename
filtered_rename = filtered_DE.rename(columns={'Value': 'Capacity (MW)'})

# Separate export and import file
filtered_export = filtered_rename[filtered_rename['Parameter'] == 'Export Capacity (MW)']
filtered_import = filtered_rename[filtered_rename['Parameter'] == 'Import Capacity (MW)']
selected_export = filtered_export.loc[:, ['Node/Line', 'Capacity (MW)']]
selected_import = filtered_import.loc[:, ['Node/Line', 'Capacity (MW)']]

## EXPORT MATRIX
# Split the "Node/Line" column into two separate columns
selected_export[['Node1', 'Node2']] = selected_export['Node/Line'].str.split('-', expand=True)

# Cutoff country names
selected_export['Node1'] = selected_export['Node1'].str.slice(0, 2)
selected_export['Node2'] = selected_export['Node2'].str.slice(0, 2)

# Aggregate double values
selected_export = selected_export.groupby(['Node1', 'Node2'])['Capacity (MW)'].sum().reset_index()

# Pivot the data to get a 2D grid with countries as row and column labels
selected_export = selected_export.pivot(index='Node1', columns='Node2', values='Capacity (MW)')
selected_export.fillna(0, inplace=True)

## IMPORT MATRIX
# Split the "Node/Line" column into two separate columns
selected_import[['Node1', 'Node2']] = selected_import['Node/Line'].str.split('-', expand=True)

# Cutoff country names
selected_import['Node1'] = selected_import['Node1'].str.slice(0, 2)
selected_import['Node2'] = selected_import['Node2'].str.slice(0, 2)

# Aggregate double values
selected_import = selected_import.groupby(['Node1', 'Node2'])['Capacity (MW)'].sum().reset_index()

# Pivot the data to get a 2D grid with countries as row and column labels
selected_import = selected_import.pivot(index='Node1', columns='Node2', values='Capacity (MW)')
selected_import.fillna(0, inplace=True)

# Export to csv
selected_export.to_csv(f"C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Demand/export_capacity_new.csv")
selected_import.to_csv(f"C:/Users/Louis/Documents/Master/Thesis/GEP/Clustering/Demand/import_capacity_new.csv")