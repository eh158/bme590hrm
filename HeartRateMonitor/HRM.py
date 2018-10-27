import numpy as np
import peakutils
import json
import os.path
import sys
from warnings import warn


def fill_metrics(metrics, data, interval):
    find_duration(metrics, data)
    find_beats(metrics, data)
    find_num_beats(metrics, data)
    find_voltage_extremes(metrics, data)
    find_mean_hr_bpm(metrics, data, interval)
    return metrics


def find_duration(metrics, data):
    time_array = data[0]
    if (len(time_array) == 0):
        metrics['duration'] = 0
        warn('No time vector detected, duration set to 0')
        return metrics
    max_time = max(time_array)
    min_time = min(time_array)
    metrics['duration'] = float(max_time - min_time) / float(60)
    if max_time < 0:
        warn('Negative time value detected, duration set to difference')
    if max_time != time_array[len(time_array) - 1]:
        warn('Max time value not last value, check time vector')
    return metrics


def find_beats(metrics, data):
    indexes = find_peaks(data[1])
    times = []
    for i in indexes:
        times.append(data[0][i])
    metrics['beats'] = times
    return metrics


def find_num_beats(metrics, data):
    indexes = find_peaks(data[1])
    metrics['num_beats'] = len(indexes)
    return metrics


def find_voltage_extremes(metrics, data):
    min_v = min(data[1])
    max_v = max(data[1])
    metrics['voltage_extremes'] = (min_v, max_v)
    return metrics


def find_mean_hr_bpm(metrics, data, time_interval):
    if time_interval > data[0][len(data[0]) - 1]:
        time_interval = data[0][len(data[0]) - 1]
    indexes = find_peaks(data[1])
    beats = 0
    for i in indexes:
        if data[0][i] <= time_interval:
            beats += 1
    mean_hr = float(beats / time_interval * 60)
    metrics['mean_hr_bpm'] = mean_hr
    return metrics


def find_peaks(voltages):
    cb = np.array(voltages)
    indexes = peakutils.indexes(cb)
    return indexes


def process_file(filename):
    csv_file = np.genfromtxt(filename, delimiter=",")
    # add checker for correct formatting, and raise exception otherwise
    if csv_file.shape[1] > 2:
        warn("Check if data is time and voltage columnwise")
    if csv_file.shape[1] < 2:
        sys.exit("Insufficient data provided; both time and voltage needed.")
    times = []
    voltages = []
    for i in csv_file:
        times.append(i[0])
        voltages.append((i[1]))
    return [times, voltages]


def gather_inputs(my_file, interval):
    data = process_file(my_file)
    metrics = {}
    input = []
    input.append(metrics)
    input.append(data)
    input.append(interval)
    return input


def get_file(my_file=None):
    if my_file is None:
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
    if type(my_file) is str:
        if ".csv" in my_file:
            return my_file
        else:
            sys.exit('File not a csv file')
    else:
        sys.exit('Filename not a string')


def process_output(metrics,filename):
    save_file = filename.replace('.csv','')
    save_file = save_file+'.json'
    with open(save_file, 'w') as outfile:
        json.dump(metrics, outfile)
    return outfile


def get_interval(interval=None):
    default_interval = 20
    if interval is None:
        while True:
            try:
                interval = input('Please specify minute interval')
                if interval.isdigit():
                    if (float(interval) <= 0):
                        print('Please specify a positive interval')
                    else:
                        break
                else:
                    raise IOError
            except IOError:
                print('Please provide a number for the interval.')
    check = str(interval).replace('.', '')
    if check.isdigit():
        if (str(interval).find(".") != str(interval).rfind(".")):
            warn('Interval invalid, default interval will be used instead')
            return default_interval
        if (float(interval) <= 0):
            warn('Interval is negative, default interval will be used instead')
            return default_interval
        return float(interval)
    else:
        warn('Interval invalid, default interval will be used instead')
        return default_interval


if __name__ == "__main__":
    # read in data from CSV file
    my_file = get_file(None)
    # read in user input for interval
    interval = get_interval(None)
    u_input = gather_inputs(my_file, float(interval))
    metrics = fill_metrics(u_input[0], u_input[1], u_input[2])
    process_output(metrics,my_file)
