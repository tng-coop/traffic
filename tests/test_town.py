import pytest

from town import Town


def test_a_star_simple_path():
    town = Town(3, 3)
    path = town.a_star((0, 0), (2, 2))
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)
    assert len(path) > 0

