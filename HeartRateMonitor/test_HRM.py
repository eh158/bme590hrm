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
    ('test', 1),
    ('test.csv', 'test.csv'),
    ('test.cvs', 1),
    ('test.vsc',1),
    (123,1),
    ('testcsv',1)
])
def test_get_file(given, expected):
    assert get_file(given) == expected