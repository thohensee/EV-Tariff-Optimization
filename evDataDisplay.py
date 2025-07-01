import pandas as pd  # array builder
import numpy as np  # array handler
import evLoadDisplay  # plots selected graphs together for comparison
import evTariffImport  # integrate tariff prices into optimization environment
import evCustomTariffs

file_path = r"C:\Users\trist\PycharmProjects\EV TOU Optimization\EV_data_case_study(Hoja2).csv"

# The 2D array is built off of the CSV file data,
# and the code adds/manipulates additional columns for logic and graphing;
# this function displays the data row-by-row in the terminal for analysis

# NOTE: use the step-by-step feature of your IDE to figure out when you want
# see_data() to execute, that will determine how many categories have been created.
# .head(x) controls how many rows display, you can take it out completely to see all
def see_data():
    for index, row in csvData.head(5).iterrows():
        print(index, row)

# Handle overnight sessions (e.g., 22 to 6)
# Vector operation (performs math on entire rows/columns)
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

# Input data from csv
csvData['ArrivalTime'] = pd.to_numeric(csvData['ArrivalTime'], errors='coerce')
csvData['DepartureTime'] = pd.to_numeric(csvData['DepartureTime'], errors='coerce')
csvData['EVSEPower_kW'] = pd.to_numeric(csvData['EVSEPower_kW'], errors='coerce')
csvData['EnergyDemand_kWh'] = pd.to_numeric(csvData['EnergyDemand_kWh'], errors='coerce')

# New column with active hours (i.e. [23, 0, 1])
csvData['ActiveHours'] = csvData.apply(get_active_hours, axis=1)

# New column for true charging duration (hours)
csvData['ChargeTime'] = csvData['EnergyDemand_kWh'] / csvData['EVSEPower_kW']


##CONTROL CENTER##
# COMMENT/UNCOMMENT SEQUENCES TO EXECUTE DIFFERENT FUNCTIONS
# NOTE: NO LINES WILL RUN AFTER LoadDisplay.plot() UNTIL YOU "X" OUT GRAPH

cheapest_hours_residential = evTariffImport.cheapest_flat_charge(csvData, 'tou')
cheapest_hours_wholesale = evTariffImport.cheapest_flat_charge(csvData, 'wholesale')

##Pre-optimized example plots##
## Flat charging as soon as car is plugged in
flat_fromStart = evLoadDisplay.get_hourly_load(np, csvData)
## Charges based on cheapest TOU tariffs offered
flat_optimized = evLoadDisplay.get_hourly_load(np, csvData, cheapest_hours_residential)
flat_optimized2 = evLoadDisplay.get_hourly_load(np, csvData, cheapest_hours_wholesale)
## NOTE: in reality wholesale tariffs would not be directly accessed by consumers,
## plot is simply demonstrative

##Systematically randomizes adjacent vehicle shifting off of peak-load hours
#evCustomTariffs.optimize_tariffs(csvData, flat_fromStart)

## Plot a single graph, or multiple
plots = [flat_fromStart, flat_optimized, flat_optimized2]
#plots = [flat_fromStart]
evLoadDisplay.plot(plots)
