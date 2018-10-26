import numpy as np
import peakutils


def find_beats(metrics, data):
    indexes = find_peaks(data[1])
    times = []
    for i in indexes:
        times.append(data[i])
    metrics['beats'] = len(times)


def find_num_beats(metrics, data):
    indexes = find_peaks(data[1])
    metrics['num_beats'] = len(indexes)


def find_voltage_extremes(metrics, data):
    min_v = min(data[1])
    max_v = max(data[1])
    metrics['voltage_extremes'] = (min_v, max_v)


def find_mean_hr_bpm(metrics, data, *args):
    if len(args) == 0:
        interval = data[0][len(data[0])]
    else:
        interval = args
    indexes = find_peaks(data[1])
    beats = 0
    for i in indexes:
        if data[0][i] <= interval:
            beats += 1
    mean_hr = float(beats)/float(interval)
    metrics['mean_hr_bpm'] = mean_hr


def find_peaks(voltages):
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
    peak_indices = find_peaks(data[0], data[1])
    print(peak_indices)
