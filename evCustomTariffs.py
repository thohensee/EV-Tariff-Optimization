import numpy as np  # array handler

##SEE GIT PUSH CAPTION FOR BREAKDOWN
def optimize_tariffs(data, transformer_load):
    hourly_load = transformer_load.copy()
    tolerance = max(data['EVSEPower_kW'])  #kW difference considered "equal enough"
    max_load_hour = np.argmax(hourly_load)
    second_max_load_hour = None

    load_copy = np.delete(hourly_load, max_load_hour)

    while second_max_load_hour == None:
    # print(max(hourly_load))
    # print(max(load_copy))
        break

    return



def is_equal(load1, load2, tolerance):
    return abs(load1 - load2) <= tolerance