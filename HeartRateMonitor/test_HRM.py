import pytest
import csv
from HRM import *


@pytest.mark.parametrize("given,expected", [
    ([0, 1, 0], 1),
    ([-1, 1, -1], 1),
    ([0, 0, 1, 0], 2)
])
def test_find_peaks(given, expected):
    assert find_peaks(given) == expected
    assert find_peaks([-2, 1, -2, -2, 0, -2])[0] == 1
    assert find_peaks([-2, 1, -2, -2, 0, -2])[1] == 4


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


@pytest.mark.parametrize("metrics, data, expected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1]], {'duration': 5 / 60}),
    ({}, [[0, 1, 2, 3, 4, 5, 5], [1, 1, 1, 1, 1, 1]], {'duration': 5 / 60}),
    ({}, [[0, 1, 2, 3, 4, 5, 6], [1, 1, 1, 1, 1, 1]], {'duration': 6 / 60}),
    ({}, [[0, 1, 2, 3, 4], [1, 1, 1, 1, 1]], {'duration': 4 / 60}),
    ({}, [[], []], {'duration': 0}),
    ({}, [[-1, 0], [1]], {'duration': 1 / 60}),
    ({}, [[-3, -2, -1], [1]], {'duration': 2 / 60}),
])
def test_find_duration(metrics, data, expected):
    assert find_duration(metrics, data) == expected


@pytest.mark.parametrize("metrics, data, expected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]}),
    ({}, [[0, 1, 2, 3, 4, 5], [1, 1, 1, 1, 1, 1]], {'beats': []})
])
def test_find_beats(metrics, data, expected):
    assert find_beats(metrics, data) == expected


@pytest.mark.parametrize("metrics, filename, jsonname, expected, exception_detected", [
    ({'beats': [1]}, 'test.csv', 'test.json', {'beats': [1]}, False),
    ({'beats': [1]}, 'test', 'test.json', {'beats': [1]}, True),
    ({'beats': [1]}, 'test.csv', 'test.json', {'beats': [1]}, True)
])
def test_process_output(metrics, filename, jsonname, expected, exception_detected):
    exception = False
    try:
        process_output(metrics, filename)
        with open(jsonname, 'r') as f:
            out = json.load(f)
        assert out == expected
    except OSError:
        exception = True
    except IOError:
        exception = True
    finally:
        assert out == expected


@pytest.mark.parametrize("filename, expected", [
    ('test0.csv', [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]])
])
def test_process_file(filename, expected):
    with open(filename, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for i in range(len(expected[0])):
            filewriter.writerow([expected[0][i], expected[1][i]])
    assert process_file(filename) == expected


@pytest.mark.parametrize("my_file, interval, expected", [
    ('test0.csv', 20, [{}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 20])
])
def test_gather_inputs(my_file, interval, expected):
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


@pytest.mark.parametrize("metrics, data, expected", [
    ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'num_beats': 2})
])
def test_find_num_beats(metrics, data, expected):
    assert find_num_beats(metrics, data) == expected


@pytest.mark.parametrize("metrics, data, interval, expected", [
    ({}, [[0, 1, 2, 3, 4], [1, 2, 1, 2, 1]], 20,
     {"duration": 0.06666666666666667, "beats": [1, 3], "num_beats": 2,
      "voltage_extremes": (1, 2), "mean_hr_bpm": 30.0})
])
def test_fill_metrics(metrics, data, interval, expected):
    assert fill_metrics(metrics, data, interval) == expected
