import pytest


@pytest.mark.parametrize("given,expected", [
    ([0, 1, 0], 1),
    ([-1, 1, -1], 1),
    ([0, 0, 1], 2)
])
def test_find_peaks(given, expected):
    from HRM import find_peaks
    assert find_peaks(given) == expected
