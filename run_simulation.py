"""Example usage of the A*-based traffic simulator."""

from town import Town, TrafficSimulator, Vehicle


def main() -> None:
    # Create a 5x5 town grid
    town = Town(width=5, height=5)

    # Adjust a few road weights to simulate traffic
    town.set_road_weight((1, 2), (2, 2), 5.0)  # heavier traffic on this road
    town.set_road_weight((2, 2), (2, 3), 3.0)

    simulator = TrafficSimulator(town)

    # Add vehicles
    vehicle1 = Vehicle(start=(0, 0), goal=(4, 4))
    vehicle2 = Vehicle(start=(4, 0), goal=(0, 4))
    simulator.add_vehicle(vehicle1)
    simulator.add_vehicle(vehicle2)

    step = 0
    while not simulator.is_complete():
        print(f"Step {step}:")
        for v in simulator.vehicles:
            print(f"  Vehicle from {v.start} to {v.goal} at {v.path[v.position_index]}")
        simulator.step()
        step += 1

    print("Simulation complete.")


if __name__ == "__main__":
    main()
