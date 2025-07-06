import pandas as pd
import random

# Import residential TOU tariffs
resTariff_path = r"C:\Users\trist\PycharmProjects\EV TOU Optimization\Spanish_residential_TOU_tariff(Hoja1)_formatted.csv"
resTariff = pd.read_csv(resTariff_path, sep=';', decimal=',', encoding='cp1252')
resTariff.columns = resTariff.columns.str.strip()

# Import wholesale marketplace tariffs
wholeTariff_path = r"C:\Users\trist\PycharmProjects\EV TOU Optimization\Wholesale_market_prices_tariff_Spain(in).csv"
wholeTariff = pd.read_csv(wholeTariff_path, sep=';', decimal=',', encoding='cp1252')
wholeTariff.columns = wholeTariff.columns.str.strip()

# Takes type-of-tariff and assigns hourly costs to active hours for each EV
# Iterates through pricing possibilities and sets charging commands for cheapest flat charge schedule
# Sends similar package to LoadDisplay for modified graph that represents the behavior of smart-charging consoles
# if user decision to immediately charge is neglected

def cheapest_flat_charge(data, tariffType = 'custom'):
    if tariffType != 'custom':
        assign_tariff(data, tariffType)

    data['CheapestOrder'] = None  # Initialize empty column

    for index, row in data.iterrows():
        cheapest_order = []
        active_hours = row['ActiveHours'].copy()
        tariff = row['Tariff'].copy()

        for hour in active_hours:
            min_tariff = min(tariff)

            # Find all indices where the tariff is equal to the minimum
            min_indices = [i for i, value in enumerate(tariff) if value == min_tariff]

            # Randomly choose one of those indices
            chosen_index = random.choice(min_indices)

            # Append the corresponding hour (not index) to the cheapest order
            cheapest_order.append(active_hours[chosen_index])

            # Remove the chosen entries to avoid repeats
            del tariff[chosen_index]
            del active_hours[chosen_index]

        # Assign entire list to dataframe cell
        data.at[index, 'CheapestOrder'] = cheapest_order

    return data['CheapestOrder']

def assign_tariff(data, tariffType):
    #These conditionals will be able to support inputs from evCustomTariffs.optimize_tariffs()
    if tariffType == 'wholesale':
        tariff = wholeTariff
    elif tariffType == 'residential':
        tariff = resTariff
    else:
        tariffType = resTariff

    # Create new column in csvData
    data['Tariff'] = [[] for _ in range(len(data))]

    # Purpose of this function is so that all active_hours have respective tariff prices for each hour
    for index, row in data.iterrows():
        active_hours = row['ActiveHours']
        tariff_list = []
        for hour in active_hours:
            tariff_list.append(float(tariff.at[hour, 'Price_€/kWh']))
        # Set the completed list into the DataFrame
        data.at[index, 'Tariff'] = tariff_list

    return data

def get_tariffs(tariffType):
    if tariffType == 'residential':
        return resTariff
    elif tariffType == 'wholesale':
        return wholeTariff
    else:
        return None



