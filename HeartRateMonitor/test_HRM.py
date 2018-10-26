import pytest
from HRM import *


@pytest.mark.parametrize("given,expected", [
    ([0, 1, 0], 1),
    ([-1, 1, -1], 1),
    ([0, 0, 1, 0], 2),
    ([-2, 1. - 2. - 2, 0. - 2], [1, 4])
])
def test_find_peaks(given, expected):
    assert find_peaks(given) == expected


@pytest.mark.parametrize("agiven,aexpected", [
    (20, 20),
    (-1, 20),
    (10, 10),
    (2.3, 2.3),
    ('2.3', 20),
    ('a', 20),
    ('helloooooo', 20)
])
def test_get_interval(agiven, aexpected):
    assert get_interval(agiven) == aexpected
