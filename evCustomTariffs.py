import numpy as np  # array handler
import math
import evLoadDisplay
import evTariffImport

def optimize_tariffs(data, load):
    shifted_graphs = []
    pool_size = 965
    hourly_load = load.copy()
    penalty_tariff = evTariffImport.get_tariffs('residential').copy()
    for i in range(50):
    # for i in range(0, 500, 100):
        custom_optimized = None

        max_load = np.max(hourly_load)
        max_index = np.argmax(hourly_load)
        min_index = np.argmin(hourly_load)

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

        if penalty_tariff.at[max_index, 'Price_€/kWh'] + 0.1 <= 0.25:
            penalty_tariff.at[max_index, 'Price_€/kWh'] += 0.1
        if penalty_tariff.at[min_index, 'Price_€/kWh'] - 0.1 >= 0.05:
            penalty_tariff.at[min_index, 'Price_€/kWh'] -= 0.1
        #print(penalty_tariff.at[0, 'Price_€/kWh'])

        # Randomly pick 100 unique indices from csvData
        random_indices = np.random.choice(data.index, size=pool_size, replace=False)

        # print(penalty_tariff)
        for index in random_indices:
            tariff = data.at[index, 'Tariff']
            #print(tariff)
            hours = data.at[index, 'ActiveHours']
            #print(hours)

            for i in range(len(tariff)):
                tariff[i] = float(penalty_tariff.at[i, 'Price_€/kWh'])

        shifted_hours = evTariffImport.cheapest_flat_charge(data, 'custom')
        shifted_hours = evLoadDisplay.get_hourly_load(np, data, 100)
        shifted_graphs.append(shifted_hours)
        hourly_load = shifted_hours
    print(penalty_tariff)

    return shifted_graphs

def chargeBehaviorProportion(data):
    flatChargePercent = 0.5

    for index, row in data.iterrows():
        break

    plot = evLoadDisplay.get_hourly_load(np, data)
    return plot


def is_equal(load1, load2, tolerance):
    return abs(load1 - load2) <= tolerance