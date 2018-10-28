import pytest
import csv
from HRM import *


@pytest.mark.parametrize("given,expected, detected", [
    ([0, 1, 0], 1, False),
    ([-1, 1, -1], 1, False),
    ([0, 0, 1, 0], 2, False),
    ([0, 1, '0'], 1, True),
    ([0, 'a', 0], 1, True)
])
def test_find_peaks(given, expected, detected):
    try:
        assert find_peaks(given) == expected
    except ValueError:
        assert detected is True
    else:
        assert find_peaks(given) == expected
        assert detected is False
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
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1]], {'duration': 5 / 60}, False),
    ({}, [[1, 2, 3, 4, 4.5, 5], [1, 1, 1, 1, 1]], {'duration': 4 / 60}, False),
    ({}, [[1, 2, 3, 4, 5, 6], [1, 1, 1, 1, 1]], {'duration': 5 / 60}, False),
    ({}, [[0, 1, 2, 3, 4], [1, 1, 1, 1, 1]], {'duration': 4 / 60}, False),
    ({}, [[], []], {'duration': 0}, False),
    ({}, [[-1, 0], [1]], {'duration': 1 / 60}, False),
    ({}, [[-3, -2, -1], [1]], {'duration': 2 / 60}, False),
    ({}, [['-3', '-2', '-1'], [1]], {'duration': 2 / 60}, True),
    ({}, [[-3, -2, 'a'], [1]], {'duration': 2 / 60}, True)
])
def test_find_duration(metrics, data, expected, detected):
    try:
        find_duration(metrics, data) == expected
    except ValueError:
        assert detected is True
    else:
        assert find_duration(metrics, data) == expected
        assert detected is False


@pytest.mark.parametrize("metrics, data, expected, detected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]}, False),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 1]], {'beats': []}, False),
    ({}, [[0, 1], [0, 'a']], {'beats': 0}, True),
    ({}, [[0, 1], ['0', '1']], {'beats': 0}, True)
])
def test_find_beats(metrics, data, expected, detected):
    try:
        find_beats(metrics, data) == expected
    except ValueError:
        assert detected is True
    else:
        assert find_beats(metrics, data) == expected
        assert detected is False


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
    ('test0.csv', [['a', 1, 2, 3, 4], [1, 2, 1, 2, 1]], True)
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
        assert expected == out


@pytest.mark.parametrize("my_file, interval, expected", [
    ('test0.csv', 20, [{}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 20])
])
def test_gather_inputs(my_file, interval, expected):
    with open(my_file, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for i in range(len(expected[0])):
            filewriter.writerow([expected[0][i], expected[1][i]])
    assert gather_inputs(my_file, interval) == expected


@pytest.mark.parametrize("metrics, data, interval, expected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], 2.5, {'mean_hr_bpm': 24.0})
])
def test_find_mean_hr_bpm(metrics, data, interval, expected):
    assert find_mean_hr_bpm(metrics, data, interval) == expected


@pytest.mark.parametrize("metrics, data, expected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]],
     {'voltage_extremes': (1, 2)}),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 1]],
     {'voltage_extremes': (1, 1)}),
    ({}, [[0, 1, 2, 3, 4, 5], []], {'voltage_extremes': ()})
])
def test_find_voltage_extremes(metrics, data, expected):
    assert find_voltage_extremes(metrics, data) == expected


@pytest.mark.parametrize("metrics, data, expected, detected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'num_beats': 2}, False),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'num_beats': 2}, False)
])
def test_find_num_beats(metrics, data, expected, detected):
    try:
        out = find_num_beats(metrics, data)
    except ValueError:
        assert detected is True
    else:
        assert out == expected
        assert detected is False


@pytest.mark.parametrize("metrics, data, interval, expected", [
    ({}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 20,
     {"duration": 0.06666666666666667, "beats": [1, 3], "num_beats": 2,
      "voltage_extremes": (1, 2), "mean_hr_bpm": 30.0})
])
def test_fill_metrics(metrics, data, interval, expected):
    assert fill_metrics(metrics, data, interval) == expected
