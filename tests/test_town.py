import pytest

from town import Town, TrafficSimulator, Vehicle


def test_a_star_simple_path():
    town = Town(3, 3)
    path = town.a_star((0, 0), (2, 2))
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)
    assert len(path) > 0


def test_vehicle_waits_at_red_signal():
    town = Town(2, 1)
    # set initial signal to red at destination
    town.nodes[(1, 0)].signal = "red"
    sim = TrafficSimulator(town)
    v = Vehicle(start=(0, 0), goal=(1, 0))
    sim.add_vehicle(v)
    sim.step()
    # vehicle should not move while signal is red
    assert v.position_index == 0
    sim.step()  # still red on second step
    assert v.position_index == 0
    sim.step()  # signal turns green
    assert v.position_index == 1

