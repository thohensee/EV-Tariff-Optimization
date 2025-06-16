import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = r"C:\Users\trist\PycharmProjects2\EV TOU Optimization\EV_data_case_study(Hoja2).csv"

# Read using correct separator and European decimal style
df = pd.read_csv(file_path, sep=';', decimal=',')

df.columns = df.columns.str.strip()
df['ArrivalTime'] = pd.to_numeric(df['ArrivalTime'], errors='coerce')
df['DepartureTime'] = pd.to_numeric(df['DepartureTime'], errors='coerce')
df['EVSEPower_kW'] = pd.to_numeric(df['EVSEPower_kW'], errors='coerce')
df['EnergyDemand_kWh'] = pd.to_numeric(df['EnergyDemand_kWh'], errors='coerce')


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

# New column with active hours
df['ActiveHours'] = df.apply(get_active_hours, axis=1)

# New column for true charging duration
df['ChargeTime'] = 0

for index, row in df.iterrows():
    df['ChargeTime'] = df['EnergyDemand_kWh'] / df['EVSEPower_kW']

# Initialize a 24-hour load profile
hourly_load = np.zeros(24)

# # Add up all EV loads at each active hour
# for _, row in df.iterrows():
#     for hour in row['ActiveHours']:
#         if not pd.isna(row['EVSEPower_kW']):
#             hourly_load[hour] += row['EVSEPower_kW']

# Add up all EV loads at each active hour
for index, row in df.iterrows():
    charge_time = row['ChargeTime']  # work on a local variable
    for hour in row['ActiveHours']:
        if charge_time > 1:
            if not pd.isna(row['EVSEPower_kW']):
                hourly_load[hour] += row['EVSEPower_kW']
                charge_time -= 1
        elif 1 > charge_time > 0:
            hourly_load[hour] += row['EVSEPower_kW'] * charge_time
            charge_time = 0
        if charge_time <= 0:
            break
    df.at[index, 'ChargeTime'] = charge_time

# Plot the histogram
plt.figure(figsize=(10, 6))
plt.bar(range(24), hourly_load, color='steelblue', width = 0.95)
plt.title('EV Charging Load on Transformer')
plt.xlabel('Hour')
plt.ylabel('Power Demand (kW)')
plt.xticks(range(24))
plt.grid(axis='y')
plt.tight_layout()
plt.show()

for index, row in df.iterrows():
    print(index, row)
#print(hourly_load)
# for _, row in df.iterrows():
#     print(row['ActiveHours'])