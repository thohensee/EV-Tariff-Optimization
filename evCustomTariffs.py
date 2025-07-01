import numpy as np  # array handler
import random

import evLoadDisplay
import evTariffImport

def optimize_tariffs(data, load):
    penalty_tariff = evTariffImport.get_tariffs('residential').copy()
    custom_optimized = None

    hourly_load = load.copy()
    max_load = np.max(hourly_load)
    max_index = np.argmax(hourly_load)

    # Use % 24 to handle circular indexing
    left_index = (max_index - 1) % 24
    right_index = (max_index + 1) % 24

    max_left = hourly_load[left_index]
    max_right = hourly_load[right_index]

    if max_left >= max_right:
        larger_difference = max_right
        shift_index = right_index
        smaller_difference = max_left
    else:
        larger_difference = max_left
        shift_index = left_index
        smaller_difference = max_right

    shift_quantity = (max_load - larger_difference) / 2

    shiftable_vehicles = []
    #hours = data['CheapestHours'].copy()

    data['ActiveChargeHours'] = []

    for index, row in data.iterrows():
        return

    for index, row in data.iterrows():
        if max_index in row['ActiveHours']:
            if shift_index in row['ActiveHours']:
                shiftable_vehicles.append(row['ActiveHours'])



    pool_size = 100
    penalty_tariff.at[max_index, 'Price_€/kWh'] += 0.01

    # Randomly pick 100 unique indices from csvData
    random_indices = np.random.choice(data.index, size=500, replace=False)

    # Set 'Tariff' to 0 for those selected rows
    data.loc[random_indices, 'Tariff'] = 0
    #
    # cheapest_hours_custom = evTariffImport.cheapest_flat_charge(data, 'custom', penalty_tariff)
    # custom_optimized = evLoadDisplay.get_hourly_load(np, data, cheapest_hours_custom)
    return hourly_load




def is_equal(load1, load2, tolerance):
    return abs(load1 - load2) <= tolerance