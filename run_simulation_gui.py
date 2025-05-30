"""GUI visualizer for the traffic simulator using tkinter.

This version creates a 10x10 grid to represent a small town and spawns
20 vehicles with random start and end points. Each vehicle is represented
as a colored rectangle moving along its planned path.
"""

import tkinter as tk
import random
from typing import List

from town import Town, TrafficSimulator, Vehicle

CELL_SIZE = 40
VEHICLE_COLORS = [
    "red",
    "blue",
    "green",
    "purple",
    "orange",
    "cyan",
    "magenta",
    "yellow",
    "pink",
    "gray",
    "brown",
    "lime",
    "navy",
    "teal",
    "maroon",
    "olive",
    "salmon",
    "gold",
    "indigo",
    "turquoise",
]


class VisualTrafficSimulator(TrafficSimulator):
    """Traffic simulator that also updates tkinter canvas visuals."""

    def __init__(self, town: Town, canvas: tk.Canvas) -> None:
        super().__init__(town)
        self.canvas = canvas
        self.vehicle_items: List[int] = []

    def add_vehicle(self, vehicle: Vehicle) -> None:
        super().add_vehicle(vehicle)
        # Create a rectangle to represent this vehicle
        color = VEHICLE_COLORS[len(self.vehicle_items) % len(VEHICLE_COLORS)]
        if vehicle.path:
            x, y = vehicle.path[0]
        else:
            x, y = vehicle.start
        item = self.canvas.create_rectangle(
            x * CELL_SIZE + 5,
            y * CELL_SIZE + 5,
            (x + 1) * CELL_SIZE - 5,
            (y + 1) * CELL_SIZE - 5,
            fill=color,
        )
        self.vehicle_items.append(item)

    def step(self) -> None:
        super().step()
        for vehicle, item in zip(self.vehicles, self.vehicle_items):
            x, y = vehicle.path[vehicle.position_index]
            self.canvas.coords(
                item,
                x * CELL_SIZE + 5,
                y * CELL_SIZE + 5,
                (x + 1) * CELL_SIZE - 5,
                (y + 1) * CELL_SIZE - 5,
            )


def draw_grid(canvas: tk.Canvas, town: Town) -> None:
    for x in range(town.width):
        for y in range(town.height):
            canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                outline="black",
            )


def main() -> None:
    # Create a larger grid to resemble a small town
    town = Town(width=10, height=10)

    # Randomly adjust a few road weights to simulate traffic
    for _ in range(15):
        a = (random.randint(0, town.width - 1), random.randint(0, town.height - 1))
        neighbors = list(town.nodes[a].neighbors.keys())
        if neighbors:
            b = random.choice(neighbors)
            town.set_road_weight(a, b, random.uniform(2.0, 6.0))

    root = tk.Tk()
    root.title("Traffic Simulator")
    canvas = tk.Canvas(root, width=town.width * CELL_SIZE, height=town.height * CELL_SIZE)
    canvas.pack()

    draw_grid(canvas, town)

    simulator = VisualTrafficSimulator(town, canvas)
    # Add 20 vehicles with random start and goal positions
    for _ in range(20):
        start = (
            random.randint(0, town.width - 1),
            random.randint(0, town.height - 1),
        )
        goal = (
            random.randint(0, town.width - 1),
            random.randint(0, town.height - 1),
        )
        while goal == start:
            goal = (
                random.randint(0, town.width - 1),
                random.randint(0, town.height - 1),
            )
        simulator.add_vehicle(Vehicle(start=start, goal=goal))

    def loop() -> None:
        if not simulator.is_complete():
            simulator.step()
            root.after(300, loop)
        else:
            print("Simulation complete.")

    root.after(300, loop)
    root.mainloop()


if __name__ == "__main__":
    main()
