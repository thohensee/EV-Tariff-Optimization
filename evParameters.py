#OPTIMIZATION PLAN
#Initial route - allocate all vehicles to cheapest window in active_hours

import pandas as pd

# Import residential TOU tariffs
resTariff_path = r"C:\Users\trist\PycharmProjects\EV TOU Optimization\Spanish_residential_TOU_tariff(Hoja1).csv"
resTariff = pd.read_csv(resTariff_path, sep=';', decimal=',', encoding='cp1252')
resTariff.columns = resTariff.columns.str.strip()

# Import wholesale marketplace tariffs
wholeTariff_path = r"C:\Users\trist\PycharmProjects\EV TOU Optimization\Wholesale_market_prices_tariff_Spain(in).csv"
wholeTariff = pd.read_csv(wholeTariff_path, sep=';', decimal=',', encoding='cp1252')
wholeTariff.columns = wholeTariff.columns.str.strip()

# Takes type-of-tariff and assigns hourly costs to active hours for each EV
# Iterates through pricing possibilities and sets charging commands for cheapest flat charge schedule
# Sends similar package to LoadDisplay for modified graph that better represents behavior of charging consoles
##INCOMPLETE (50%)##
def organize_cheapest(data, tariffType):
    active_hours = data['ActiveHours']
    charge_time = data['ChargeTime']
    if tariffType == 'wholesale':
        tariff = wholeTariff
    elif tariffType == 'tou':
        tariff = resTariff
    else:
        tariff = resTariff
    data['Tariff'] = 0.0
    for index, row in data.iterrows():
        for i in range(len(row['ActiveHours'])):
            hour = row['ActiveHours'][i]
            #print(f"row['ActiveHours'][{i}] = {hour}")
            #print(f"Tariff = ", tariff.iloc[hour]['Price_€/kW'])
            data.at[index, 'Tariff'] = tariff.iloc[hour]['Price_€/kW']
    print(data['Tariff'])

# def set_start_hour():
#     return

# FOR MONDAY/TUESDAY: Inputs modified tariff specifications to send to organize_cheapest()
# Possibly add smoothing logic to dynamically shave off humps and allocate toward valleys
def optimize_shift():
    return


#print(wholeTariff)
# for row, index in tariffData.head(5).iterrows():
#     print(index, row)
#     print('\n')


