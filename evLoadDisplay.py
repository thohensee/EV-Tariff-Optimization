import matplotlib.pyplot as plt  #Code for graphing

def get_hourly_load(np, data, cheapest_hours = None):
    # Initialize a 24-hour load profile
    hourly_load = np.zeros(24)
    # Add up all EV loads at each active hour
    for index, row in data.iterrows():
        charge_time = row['ChargeTime']  # work on a local variable

        if cheapest_hours is None:
            hours = row['ActiveHours'].copy()
        else:
            hours = cheapest_hours.loc[index].copy()

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

    for plot in plots:
        plt.plot(range(24), plot, marker='o', linestyle='-', color='steelblue')

    plt.title('EV Charging Load on Transformer')
    plt.xlabel('Hour')
    plt.ylabel('Power Demand (kW)')
    plt.xticks(range(24))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# # Array data sent to console
# for index, row in df.iterrows():
#     print(index, row)