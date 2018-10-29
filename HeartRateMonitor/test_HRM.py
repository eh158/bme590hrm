import pytest
import csv
from HRM import *


@pytest.mark.parametrize("given,expected, detected", [
    ([0, 1, 0], 1, False),
    ([-1, 1, -1], 1, False),
    ([0, 0, 1, 0], 2, False),
    ([0, 0, '1', 0], 2, True)
])
def test_find_peaks(given, expected, detected):
    try:
        out = find_peaks(given)
    except ValueError:
        assert detected is True
    else:
        assert detected is False
        assert out == expected
    # assert find_peaks([-2, 1, -2, -2, 0, -2])[0] == 1
    # assert find_peaks([-2, 1, -2, -2, 0, -2])[1] == 4


@pytest.mark.parametrize("agiven,aexpected", [
    (20, 20),
    (-1, 20),
    (10, 10),
    (2.3, 2.3),
    ('2.3', 2.3),
    ('a', 20),
    ('helloooooo', 20),
    ('2 3', 20),
    ('.23.', 20),
    ('.2.2.25.5.5.5.5.5.5', 20)
])
def test_get_interval(agiven, aexpected):
    assert get_interval(agiven) == aexpected


@pytest.mark.parametrize("given,expected", [
    ('test.csv', 'test.csv'),
])
def test_get_file(given, expected):
    assert get_file(given) == expected


# @pytest.mark.parametrize("given", [
#     ('test.cvs'),
#     ('test.vsc'),
#     (123),
#     ('testcsv'),
# ])
# def test_get_file_exit(given):
#     with pytest.raises(SystemExit) as pytest_wrapped_e:
#         get_file(given)
#     assert pytest_wrapped_e.type == SystemExit
#     assert pytest_wrapped_e.value.code == 1


@pytest.mark.parametrize("metrics, data, expected, detected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1]],
     {'duration': 5 / 60}, False),
    ({}, [[0, 1, 2, 3, 4, 5, 5], [1, 1, 1, 1, 1, 1]],
     {'duration': 5 / 60}, False),
    ({}, [[0, 1, 2, 3, 4, 5, 6], [1, 1, 1, 1, 1, 1]],
     {'duration': 6 / 60}, False),
    ({}, [[0, 1, 2, 3, 4], [1, 1, 1, 1, 1]],
     {'duration': 4 / 60}, False),
    ({}, [[], []], {'duration': 0}, False),
    ({}, [[-1, 0], [1]], {'duration': 1 / 60}, False),
    ({}, [[-3, -2, -1], [1]], {'duration': 2 / 60}, False),
    ({}, [[0, 1, 2, 3, '4'], [1, 1, 1, 1, 1]],
     {'duration': 4 / 60}, True),
])
def test_find_duration(metrics, data, expected, detected):
    try:
        out = find_duration(metrics, data)
    except ValueError:
        assert detected is True
    else:
        assert detected is False
        assert out == expected


@pytest.mark.parametrize("metrics, data, expected, detected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]}, False),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 1]], {'beats': []}, False),
    ({}, [[0, 1, 2, 3, '4'], [1, 1, 1, 1, '1']], {'beats': []}, True)
])
def test_find_beats(metrics, data, expected, detected):
    try:
        out = find_beats(metrics, data)
    except ValueError:
        assert detected is True
    else:
        assert detected is False
        assert out == expected


@pytest.mark.parametrize("metrics, filename, f2, jn, expected, detected", [
    ({'beats': [1]}, 't.csv', 't.csv', 't.json', {'beats': [1]}, False),
    ({'beats': [1]}, 200, 't.csv', 't.json', {'beats': [1]}, True),
    ({'beats': [1]}, 't1.csv', 't.csv', 't.json', {'beats': [1]}, True)
])
def test_process_output(metrics, filename, f2, jn, expected, detected):
    with open(f2, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for i in range(5):
            filewriter.writerow([i, i % 2])
    try:
        process_output(metrics, filename)
    except ValueError:
        assert detected is True
    else:
        with open(jn, 'r') as f:
            out = json.load(f)
        assert out == expected


@pytest.mark.parametrize("filename, expected, detected", [
    ('test0.csv', [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], False),
    ('test0.csv', [[0, 1, 2, 3, 4], ['a', 2, 1, 2, 1]], True)
])
def test_process_file(filename, expected, detected):
    with open(filename, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for i in range(len(expected[0])):
            filewriter.writerow([expected[0][i], expected[1][i]])
    try:
        out = process_file(filename)
    except ValueError:
        assert detected is True
    else:
        assert detected is False
        assert out == expected


@pytest.mark.parametrize("my_file, interval, expected, detected", [
    ('test0.csv', 16, [{}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 16], False),
    ('test0', 16, [{}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 16], True),
    ('0', 16, [{}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 16], True),
    (0, 16, [{}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 16], True),
    ('test4.csv', 16, [{}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 16], True)
])
def test_gather_inputs(my_file, interval, expected, detected):
    try:
        out = gather_inputs(my_file, interval)
    except OSError:
        assert detected is True
    except IOError:
        assert detected is True
    except ValueError:
        assert detected is True
    else:
        assert out == expected
        assert detected is False


@pytest.mark.parametrize("metrics, data, interval, expected, detected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]],
     2.5, {'mean_hr_bpm': 24.0}, False),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, '1']],
     2.5, {'mean_hr_bpm': 24.0}, True),
    ({}, [[0, 1, 2, 3, 4, '5'], [1, 2, 1, 2, 1]],
     2.5, {'mean_hr_bpm': 24.0}, True)
])
def test_find_mean_hr_bpm(metrics, data, interval, expected, detected):
    try:
        out = find_mean_hr_bpm(metrics, data, interval)
    except ValueError:
        assert detected is True
    else:
        assert detected is False
        assert out == expected


@pytest.mark.parametrize("metrics, data, expected, detected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]],
     {'voltage_extremes': (1, 2)}, False),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 1]],
     {'voltage_extremes': (1, 1)}, False),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, '1']],
     {'voltage_extremes': (1, 1)}, True),
    ({}, [[0, 1, 2, 3, 4, 5], []], {'voltage_extremes': ()}, False)
])
def test_find_voltage_extremes(metrics, data, expected, detected):
    try:
        out = find_voltage_extremes(metrics, data)
    except ValueError:
        assert detected is True
    else:
        assert detected is False
        assert out == expected


@pytest.mark.parametrize("metrics, data, expected, detected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'num_beats': 2}, False),
    ({}, [[0, 1, 2, 3, '4'], [1, 2, 1, 2, '1']], {'num_beats': 2}, True)
])
def test_find_num_beats(metrics, data, expected, detected):
    try:
        out = find_num_beats(metrics, data)
    except ValueError:
        assert detected is True
    else:
        assert detected is False
        assert out == expected


@pytest.mark.parametrize("metrics, data, interval, expected", [
    ({}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 20,
     {"duration": 0.06666666666666667, "beats": [1, 3], "num_beats": 2,
      "voltage_extremes": (1, 2), "mean_hr_bpm": 30.0})
])
def test_fill_metrics(metrics, data, interval, expected):
    assert fill_metrics(metrics, data, interval) == expected


# if __name__ == "__main__":
#     expected = [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]]
#     with open('abc.csv', 'w') as csvfile:
#         filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
#                                 quoting=csv.QUOTE_MINIMAL)
#         for i in range(len(expected[0])):
#             filewriter.writerow([expected[0][i], expected[1][i]])
#     csv_file = np.genfromtxt('abc.csv', delimiter=",", dtype=None)
#     print(csv_file)
#     print(len(csv_file.shape))