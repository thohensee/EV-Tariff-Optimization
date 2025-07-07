import matplotlib.pyplot as plt  #Code for graphing
import random
import math
from matplotlib.colors import CSS4_COLORS
import pandas as pd

baseLoad_path = r"C:\Users\trist\PycharmProjects\EV TOU Optimization\Residential_base_demand(in).csv"
baseLoad = pd.read_csv(baseLoad_path, sep=';', decimal=',', encoding='cp1252')
baseLoad.columns = baseLoad.columns.str.strip()

random_indices = []

# def get_hourly_load(np, data, flat_percent = None):
#     # Initialize a 24-hour load profile
#     hourly_load = np.zeros(24)
#     # Add up all EV loads at each active hour
#     for index, row in data.iterrows():
#         charge_time = row['ChargeTime']  # work on a local variable
#
#         if flat_percent is None:
#             hours = row['ActiveHours'].copy()
#         else:
#             hours = row['CheapestOrder'].copy()
#
#         for hour in hours:
#             if charge_time > 1:
#                 hourly_load[hour] += row['EVSEPower_kW']
#                 charge_time -= 1
#             elif 1 > charge_time > 0:
#                 hourly_load[hour] += row['EVSEPower_kW'] * charge_time
#                 charge_time = 0
#             if charge_time <= 0:
#                 break
#     return hourly_load

def get_hourly_load(np, data, cheapest_percent = 0):
    # Initialize a 24-hour load profile
    hourly_load = np.zeros(24)
    random_indices = []
    hours = None

    # Apply base residential household on transformer
    for hour in range(24):
        hourly_load[hour] += baseLoad.at[hour, 'Demand_kWh']

    if cheapest_percent != None:
        cheapest_percent = cheapest_percent / 100
        pool_size = math.floor(len(data) * cheapest_percent)
        random_indices = np.random.choice(data.index, size=pool_size, replace=False)

    # Add up all EV loads at each active hour
    for index, row in data.iterrows():
        charge_time = row['ChargeTime']  # work on a local variable

        if cheapest_percent is None:
            hours = row['ActiveHours'].copy()
        else:
            if index in random_indices:
                hours = row['CheapestOrder'].copy()
            else:
                hours = row['ActiveHours'].copy()

        for hour in hours:
            if charge_time > 1:
                hourly_load[hour] += row['EVSEPower_kW']
                charge_time -= 1
            elif 1 > charge_time > 0:
                hourly_load[hour] += row['EVSEPower_kW'] * charge_time
                charge_time = 0
            if charge_time <= 0:
                break
    return hourly_load

# Plot Line Graph
# Ensure simultaneous graphing capability
def plot(plots):
    plt.figure(figsize=(10, 6))
    max_loads = []

    # First, calculate peak loads
    for plot in plots:
        max_loads.append(max(plot))

    # Find the index with the lowest peak load
    min_index = max_loads.index(min(max_loads))

    for i, plot in enumerate(plots):
        if i == 0:
            color = 'red'
        elif i == 1:
            color = 'green'
        elif i == min_index:
            color = 'yellow'  # Best peak load reduction
        elif i == len(plots) - 1:
            color = 'black'
        else:
            color = 'orange'

        plt.plot(range(24), plot, marker='o', linestyle='-', color=color)

    print(max(plots[0]) - min(max_loads))

    plt.title('EV Charging Load on Transformer')
    plt.xlabel('Hour')
    plt.ylabel('Power Demand (kW)')
    plt.xticks(range(24))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Random hex color
def random_color():
    return random.choice(list(CSS4_COLORS.keys()))