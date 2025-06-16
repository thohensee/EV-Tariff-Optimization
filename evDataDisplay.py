import pandas as pd  # array handler
import numpy as np  # array builder
import LoadDisplay  # graphs histogram

file_path = r"C:\Users\trist\PycharmProjects2\EV TOU Optimization\EV_data_case_study(Hoja2).csv"


# Handle overnight sessions (e.g., 22 to 6)
def get_active_hours(row):
    start = int(row['ArrivalTime']) % 24
    end = int(row['DepartureTime']) % 24
    if start == end:
        return list(range(24))  # Full day
    if start < end:
        return list(range(start, end + 1))
    else:
        return list(range(start, 24)) + list(range(0, end + 1))

# Read using correct separator and European decimal style
csvData = pd.read_csv(file_path, sep=';', decimal=',')

## CONVERT CSV DATA INTO 2D ARRAY WITH ADDED COLUMNS ##
csvData.columns = csvData.columns.str.strip()
csvData['ArrivalTime'] = pd.to_numeric(csvData['ArrivalTime'], errors='coerce')
csvData['DepartureTime'] = pd.to_numeric(csvData['DepartureTime'], errors='coerce')
csvData['EVSEPower_kW'] = pd.to_numeric(csvData['EVSEPower_kW'], errors='coerce')
csvData['EnergyDemand_kWh'] = pd.to_numeric(csvData['EnergyDemand_kWh'], errors='coerce')

# New column with active hours (i.e. [23, 0, 1])
csvData['ActiveHours'] = csvData.apply(get_active_hours, axis=1)

# New column for true charging duration (hours)
csvData['ChargeTime'] = 0

for index, row in csvData.iterrows():
    csvData['ChargeTime'] = csvData['EnergyDemand_kWh'] / csvData['EVSEPower_kW']


hourly_load = LoadDisplay.hourly_load(np, csvData, pd)
LoadDisplay.plot(hourly_load)





##OLD LINES##

## Add up all EV loads at each active hour
# for _, row in df.iterrows():
#     for hour in row['ActiveHours']:
#         if not pd.isna(row['EVSEPower_kW']):
#             hourly_load[hour] += row['EVSEPower_kW']
