import numpy as np
import peakutils
import json
import os.path
import sys
import csv
import logging
from warnings import warn


def fill_metrics(metrics, data, interval):
    find_duration(metrics, data)
    find_beats(metrics, data)
    find_num_beats(metrics, data)
    find_voltage_extremes(metrics, data)
    find_mean_hr_bpm(metrics, data, interval)
    return metrics


def find_duration(metrics, data):
    x = [i for i in data[0] if isinstance(i, str)]
    if len(x) > 0:
        raise ValueError('String not expected')
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
    x = [i for i in data[1] if isinstance(i, str)]
    if len(x) > 0:
        logging.error('String not expected')
        raise ValueError('String not expected')
    indexes = find_peaks(data[1])
    times = []
    for i in indexes:
        times.append(data[0][i])
    metrics['beats'] = times
    return metrics


def find_num_beats(metrics, data):
    x = [i for i in data[1] if isinstance(i, str)]
    if len(x) > 0:
        logging.error('String not expected')
        raise ValueError('String not expected')
    indexes = find_peaks(data[1])
    metrics['num_beats'] = len(indexes)
    return metrics


def find_voltage_extremes(metrics, data):
    x = [i for i in data[1] if isinstance(i, str)]
    if len(x) > 0:
        logging.error('String not expected')
        raise ValueError('String not expected')
    if (len(data[1]) == 0):
        metrics['voltage_extremes'] = ()
        warn('No voltage data available')
        return metrics
    min_v = min(data[1])
    max_v = max(data[1])
    metrics['voltage_extremes'] = (min_v, max_v)
    return metrics


def find_mean_hr_bpm(metrics, data, time_interval):
    x = [i for i in data[0] if isinstance(i, str)]
    y = [i for i in data[1] if isinstance(i, str)]
    if len(x) > 0 or len(y) > 0:
        logging.error('String not expected')
        raise ValueError('String not expected')
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
    x = [i for i in voltages if isinstance(i, str)]
    if len(x) > 0:
        logging.error('String not expected')
        raise ValueError('String not expected')
    cb = np.array(voltages)
    indexes = peakutils.indexes(cb)
    return indexes


def process_file(filename):
    if not isinstance(filename, str):
        logging.error('File not string')
        raise IOError('File not string')
    elif not os.path.isfile(filename):
        logging.error('File not found')
        raise OSError('File not found')
    elif ".csv" not in filename:
        logging.error('File not csv file')
        raise IOError('File not csv file')
    csv_file = np.genfromtxt(filename, delimiter=",", dtype=None)
    # add checker for correct formatting, and raise exception otherwise
    if len(csv_file.shape) > 1:
        if csv_file.shape[1] > 2:
            logging.warn('More data provided than needed')
            warn("Check if data is time and voltage columnwise")
        if csv_file.shape[1] < 2:
            logging.error('Data format incorrect')
            sys.exit("Insufficient data; both time and voltage needed.")
    else:
        raise ValueError('Strings detected in data or data format wrong.')
    times = []
    voltages = []
    for i in csv_file:
        if not isinstance(i[0], str):
            times.append(i[0])
        if not isinstance(i[1], str):
            voltages.append((i[1]))
    return [times, voltages]


def gather_inputs(my_file, interval):
    if not isinstance(my_file, str):
        logging.error('File not string')
        raise IOError('File not string')
    elif '.csv' not in my_file:
        logging.error('File not csv file')
        raise IOError('File not csv file')
    data = process_file(my_file)
    metrics = {}
    input = []
    input.append(metrics)
    input.append(data)
    input.append(interval)
    return input


def get_file(my_file=None):
    logging.basicConfig(filename="megatslog.txt",
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
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
            logging.info('File valid')
            return my_file
        else:
            logging.error('File invalid.')
            sys.exit('File not csv file, exiting now.')
    else:
        logging.error('File invalid')
        sys.exit('Filename not a string, exiting now')


def process_output(metrics, filename):
    if (isinstance(filename, str) is False):
        raise ValueError
    try:
        if os.path.isfile(filename):
            if ".csv" in filename:
                pass
            else:
                raise IOError
        else:
            raise OSError
    except IOError:
        print('Please specify a csv file.')
        logging.error('Not a csv file')
    except OSError:
        print('File not found')
        logging.error('File not found')
    if (len(list(metrics.keys())) == 0):
        warn('No data was processed')
    save_file = filename.replace('.csv', '')
    save_file = save_file + '.json'
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
            logging.warn('Default interval used')
            return default_interval
        if (float(interval) <= 0):
            warn('Interval is negative, default interval will be used instead')
            logging.warn('Default interval used')
            return default_interval
        return float(interval)
    else:
        warn('Interval invalid, default interval will be used instead')
        logging.warn('Default interval used')
        return default_interval


if __name__ == "__main__":
    # read in data from CSV file
    my_file = get_file('ab')
    # read in user input for interval
    interval = get_interval(None)
    u_input = gather_inputs(my_file, float(interval))
    metrics = fill_metrics(u_input[0], u_input[1], u_input[2])
    process_output(metrics, my_file)
    a = process_output({'beats': [1]}, 'test.csv')
    # filename = 't.csv'
    # expected = [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]]
    # with open(filename, 'w') as csvfile:
    #     filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
    # quoting=csv.QUOTE_MINIMAL)
    #     for i in range(len(expected[0])):
    #         filewriter.writerow([expected[0][i],expected[1][i]])
    # b = gather_inputs(filename, 20)
