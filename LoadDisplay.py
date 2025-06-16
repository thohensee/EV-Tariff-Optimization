import matplotlib.pyplot as plt  #Code for graphin

def hourly_load(np, csvData, pd):
    # Initialize a 24-hour load profile
    hourly_load = np.zeros(24)

    # Add up all EV loads at each active hour
    for index, row in csvData.iterrows():
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
        csvData.at[index, 'ChargeTime'] = charge_time
    return hourly_load

# Plot histogram
def plot(hourly_load):
    plt.figure(figsize=(10, 6))
    plt.bar(range(24), hourly_load, color='steelblue', width = 0.95)
    plt.title('EV Charging Load on Transformer')
    plt.xlabel('Hour')
    plt.ylabel('Power Demand (kW)')
    plt.xticks(range(24))
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# # Array data sent to console
# for index, row in df.iterrows():
#     print(index, row)