import numpy as np  # array handler
import math
import evLoadDisplay
import evTariffImport
import pandas as pd

baseLoad_path = r"C:\Users\trist\PycharmProjects\EV TOU Optimization\Residential_base_demand(in).csv"
baseLoad = pd.read_csv(baseLoad_path, sep=';', decimal=',', encoding='cp1252')
baseLoad.columns = baseLoad.columns.str.strip()

def optimize_tariffs(data, load, participants):
    momentum = np.zeros(24)  # Momentum vector for each hour
    beta = 0.9  # Momentum factor (controls memory)
    lr = 0.05  # Learning rate for tariff update
    min_price = 0.00  # €/kWh
    max_price = 0.2  # €/kWh
    shifted_graphs = []
    pool_size = participants
    hourly_load = load.copy()

    # Randomly pick 100 unique indices from csvData
    random_indices = np.random.choice(data.index, size=pool_size, replace=False)

    # Apply base residential household on transformer
    for hour in range(24): ##DONT ACCIDENTALLY CHANGE##
        hourly_load[hour] += baseLoad.at[hour, 'Demand_kWh']

    penalty_tariff = evTariffImport.get_tariffs('tou').copy()

    threshold = 0.1  # kW difference tolerance
    previous_load = np.array(hourly_load)

    for i in range(50):
        # for i in range(0, 500, 100):
        custom_optimized = None

        # Smooth the load profile using rolling average (window=3)
        smoothed_load = pd.Series(hourly_load).rolling(window=3, center=True, min_periods=1).mean().to_numpy()

        # Find max and min load hours from smoothed data
        max_index = np.argmax(smoothed_load)
        min_index = np.argmin(smoothed_load)

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

        load_diff = hourly_load - np.mean(hourly_load)  # Pressure to balance load
        momentum = beta * momentum + (1 - beta) * load_diff

        # Update prices based on momentum (gradient descent analogy)
        penalty_tariff['Price_€/kWh'] -= lr * momentum

        # Clip prices to your allowed range
        penalty_tariff['Price_€/kWh'] = penalty_tariff['Price_€/kWh'].clip(lower=min_price, upper=max_price)


        # # Randomly pick 100 unique indices from csvData
        # random_indices = np.random.choice(data.index, size=pool_size, replace=False)

        # random_indices = evLoadDisplay.random_indices

        # print(penalty_tariff)
        for index in random_indices:
            tariff = data.at[index, 'Tariff']
            # print(tariff)
            hours = data.at[index, 'ActiveHours']
            # print(hours)

            for i in range(len(tariff)):
                tariff[i] = float(penalty_tariff.at[i, 'Price_€/kWh'])

        evTariffImport.cheapest_flat_charge(data, 'custom')
        shifted_hours = evLoadDisplay.get_hourly_load(np, data, random_indices)
        shifted_graphs.append(shifted_hours)
        hourly_load = shifted_hours

        # Change detection
        diff = abs(np.max(shifted_hours) - np.max(previous_load))
        if diff < threshold:
            print(f"Converged after {i} iterations. Δ = {diff:.4f} kW")
            break

        previous_load = np.array(shifted_hours)
        hourly_load = shifted_hours
    print(penalty_tariff)

    return shifted_graphs

# def optimize_tariffs(data, load):
#     shifted_graphs = []
#     pool_size = 500
#     hourly_load = load.copy()
#
#     # Randomly pick 100 unique indices from csvData
#     random_indices = np.random.choice(data.index, size=pool_size, replace=False)
#
#     # Apply base residential household on transformer
#     for hour in range(24):
#         hourly_load[hour] += baseLoad.at[hour, 'Demand_kWh']
#
#     penalty_tariff = evTariffImport.get_tariffs('tou').copy()
#
#     threshold = 0.1  # kW difference tolerance
#     previous_load = np.array(hourly_load)
#
#     for i in range(100):
#         # for i in range(0, 500, 100):
#         custom_optimized = None
#
#         max_load = np.max(hourly_load)
#         max_index = np.argmax(hourly_load)
#         min_index = np.argmin(hourly_load)
#
#         # Use % 24 to handle circular indexing
#         left_index = (max_index - 1) % 24
#         right_index = (max_index + 1) % 24
#
#         max_left = hourly_load[left_index]
#         max_right = hourly_load[right_index]
#
#         if max_left >= max_right:
#             larger_difference = max_right
#             shift_index = right_index
#             smaller_difference = max_left
#         else:
#             larger_difference = max_left
#             shift_index = left_index
#             smaller_difference = max_right
#
#         if penalty_tariff.at[max_index, 'Price_€/kWh'] + 0.1 <= 0.25:
#             penalty_tariff.at[max_index, 'Price_€/kWh'] += 0.1
#         if penalty_tariff.at[min_index, 'Price_€/kWh'] - 0.1 >= 0.05:
#             penalty_tariff.at[min_index, 'Price_€/kWh'] -= 0.1
#         # print(penalty_tariff.at[0, 'Price_€/kWh'])
#
#         # # Randomly pick 100 unique indices from csvData
#         # random_indices = np.random.choice(data.index, size=pool_size, replace=False)
#
#         # random_indices = evLoadDisplay.random_indices
#
#         # print(penalty_tariff)
#         for index in random_indices:
#             tariff = data.at[index, 'Tariff']
#             # print(tariff)
#             hours = data.at[index, 'ActiveHours']
#             # print(hours)
#
#             for i in range(len(tariff)):
#                 tariff[i] = float(penalty_tariff.at[i, 'Price_€/kWh'])
#
#         shifted_hours = evTariffImport.cheapest_flat_charge(data, 'custom')
#         shifted_hours = evLoadDisplay.get_hourly_load(np, data, 100)
#         shifted_graphs.append(shifted_hours)
#         hourly_load = shifted_hours
#     print(penalty_tariff)
#
#     return shifted_graphs
