import pytest
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

# @pytest.mark.parametrize("metrics, data, expected", [
#     ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]})
# ])
# def test_process_output(metrics, filename, expected):
#     assert process_output(metrics, filename) == expected
#
#
# @pytest.mark.parametrize("metrics, data, expected", [
#     ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]})
# ])
# def test_gather_inputs(metrics, data, expected):
#     assert gather_inputs(metrics, data) == expected
#
#
# @pytest.mark.parametrize("metrics, data, expected", [
#     ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]})
# ])
# def test_find_mean_hr(metrics, data, expected):
#     assert find_mean_hr(metrics, data) == expected
#
#
# @pytest.mark.parametrize("metrics, data, expected", [
#     ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]})
# ])
# def test_find_voltage_extremes(metrics, data, expected):
#     assert find_voltage_extremes(metrics, data) == expected
#
#
# @pytest.mark.parametrize("metrics, data, expected", [
#     ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]})
# ])
# def test_find_num_beats(metrics, data, expected):
#     assert find_num_beats(metrics, data) == expected
#
#
# @pytest.mark.parametrize("metrics, data, expected", [
#     ({}, [[0, 1, 2, 3, 4, 5], [1, 2, 1, 2, 1, 1]], {'beats': [1, 3]})
# ])
# def test_fill_metrics(metrics, data, expected):
#     assert fill_metrics(metrics, data) == expected
