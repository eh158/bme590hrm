import numpy as np
import peakutils
import json
import os.path


def fill_metrics(metrics, data, interval):
    find_duration(metrics, data)
    find_beats(metrics, data)
    find_num_beats(metrics, data)
    find_voltage_extremes(metrics, data)
    find_mean_hr_bpm(metrics, data, interval)
    return metrics


def find_duration(metrics, data):
    time_array = data[0]
    time = float(time_array[len(time_array)-1]) / float(60)
    metrics['duration'] = time


def find_beats(metrics, data):
    indexes = find_peaks(data[1])
    times = []
    for i in indexes:
        times.append(data[0][i])
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
        interval = data[0][len(data[0])-1]
    else:
        interval = args
    indexes = find_peaks(data[1])
    beats = 0
    for i in indexes:
        if data[0][i] <= interval[0]:
            beats += 1
    mean_hr = float(beats/interval[0]*60)
    metrics['mean_hr_bpm'] = mean_hr


def find_peaks(voltages):
    cb = np.array(voltages)
    indexes = peakutils.indexes(cb)
    return indexes


def process_file(filename):
    csv_file = np.genfromtxt(my_file, delimiter=",")
    # add checker for correct formatting, and raise exception otherwise
    times = []
    voltages = []
    for i in csv_file:
        times.append(i[0])
        voltages.append(i[1])
    return [times, voltages]


def gather_inputs(my_file, interval):
    data = process_file(my_file)
    if(interval<0):
        interval = 20
    metrics = {}
    input = []
    input.append(metrics)
    input.append(data)
    input.append(interval)
    return input


if __name__ == "__main__":
    print("HRM")
    # read in data from CSV file
    while True:
        try:
            my_file = input('Please specify the filename.\n')
            if os.path.isfile(my_file):
                if ".csv" in my_file:
                    break
                raise IOError
            else:
                print('File not found')
        except IOError:
            print('Please specify a csv file.')
    # read in user input for interval
    while True:
        try:
            interval = input('Please specify minute interval')
            if interval.isdigit():
                if(float(interval)<=0):
                    print('Please specify a positive interval')
                else:
                    break
            else:
                raise IOError
        except IOError:
            print('Please provide a number for the interval.')
    u_input = gather_inputs(my_file, float(interval))
    metrics = fill_metrics(u_input[0],u_input[1],u_input[2])
    print(metrics)
