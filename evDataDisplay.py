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
    for index, row in data.head(5).iterrows():
        print(index, row)

def get_plots():
    return plots

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
data = pd.read_csv(file_path, sep=';', decimal=',')

## CONVERT CSV DATA INTO 2D ARRAY WITH ADDED COLUMNS ##
data.columns = data.columns.str.strip()

# Input data from csv
data['ArrivalTime'] = pd.to_numeric(data['ArrivalTime'], errors='coerce')
data['DepartureTime'] = pd.to_numeric(data['DepartureTime'], errors='coerce')
data['EVSEPower_kW'] = pd.to_numeric(data['EVSEPower_kW'], errors='coerce')
data['EnergyDemand_kWh'] = pd.to_numeric(data['EnergyDemand_kWh'], errors='coerce')

# New column with active hours (i.e. [23, 0, 1])
data['ActiveHours'] = data.apply(get_active_hours, axis=1)

# New column for true charging duration (hours)
data['ChargeTime'] = data['EnergyDemand_kWh'] / data['EVSEPower_kW']


##CONTROL CENTER##
# COMMENT/UNCOMMENT SEQUENCES TO EXECUTE DIFFERENT FUNCTIONS
# NOTE: NO LINES WILL RUN AFTER LoadDisplay.plot() UNTIL YOU "X" OUT GRAPH
# Create new column in csvData

cheapest_hours_residential = evTariffImport.cheapest_flat_charge(data, 'residential')
cheapest_hours_wholesale = evTariffImport.cheapest_flat_charge(data, 'wholesale')
flat_optimized2 = evLoadDisplay.get_hourly_load(np, data, cheapest_hours_wholesale)

##Pre-optimized example plots##
## Flat charging as soon as car is plugged in
flat_fromStart = evLoadDisplay.get_hourly_load(np, data)
## Charges based on cheapest TOU tariffs offered
flat_res_cheapest = evLoadDisplay.get_hourly_load(np, data, cheapest_hours_residential)

## NOTE: in reality wholesale tariffs would not be directly accessed by consumers,
## plot is simply demonstrative

#print(max(csvData['EVSEPower_kW']))

## Plot a single graph, or multiple
plots = [flat_fromStart, flat_res_cheapest]
#plots = [flat_fromStart]
#plots = [flat_res_cheapest]

##Systematically randomizes adjacent vehicle shifting off of peak-load hours
#plots.append(evCustomTariffs.optimize_tariffs(data, flat_res_cheapest))

evLoadDisplay.plot(plots)