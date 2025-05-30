"""Example usage of the A*-based traffic simulator."""

from typing import List

from town import Town, TrafficSimulator, Vehicle


def render_town(town: Town, vehicles: List[Vehicle]) -> None:
    """Render an ASCII representation of the town with vehicles and signals."""
    def color(x: int, y: int) -> str:
        sig = town.nodes[(x, y)].signal
        return {
            "green": "G",
            "yellow": "Y",
            "red": "R",
        }[sig]

    grid = [[color(x, y) for x in range(town.width)] for y in range(town.height)]
    for idx, vehicle in enumerate(vehicles, start=1):
        if vehicle.path:
            x, y = vehicle.path[vehicle.position_index]
            # Show vehicle index at its current position
            grid[y][x] = str(idx)

    for row in grid:
        print(" ".join(row))
    print()


def main() -> None:
    # Create a larger town with random roads and signal phases
    town = Town(
        width=7,
        height=7,
        randomize_signals=True,
        random_roads=True,
    )

    simulator = TrafficSimulator(town)

    # Add a few vehicles
    starts_goals = [
        ((0, 0), (6, 6)),
        ((6, 0), (0, 6)),
        ((3, 6), (6, 3)),
        ((0, 3), (6, 0)),
    ]
    for s, g in starts_goals:
        simulator.add_vehicle(Vehicle(start=s, goal=g))

    step = 0
    MAX_STEPS = 15
    while step < MAX_STEPS and not simulator.is_complete():
        print(f"Step {step}:")
        render_town(town, simulator.vehicles)
        for v in simulator.vehicles:
            print(f"  Vehicle from {v.start} to {v.goal} at {v.path[v.position_index]}")
        simulator.step()
        step += 1

    print("Demo complete.")


if __name__ == "__main__":
    main()
