import numpy as np
import peakutils


def find_beats():
    return 0


def find_num_beats():
    return 0


def find_voltage_extremes():
    return 0


def find_mean_hr_bpm():
    return 0


def find_peaks(time,voltages):
    cb = np.array(voltages)
    indexes = peakutils.indexes(cb)
    return indexes


def process_file(filename):
    csv_file = np.genfromtxt(my_file, delimiter=",")
    times = []
    voltages = []
    for i in csv_file:
        times.append(i[0])
        voltages.append(i[1])
    return [times, voltages]


if __name__ == "__main__":
    print("HRM")
    # read in data from CSV file
    my_file = "test1.csv"
    data = process_file(my_file)
    peak_indices = find_peaks(data[0],data[1])
    print(peak_indices)