"""GUI visualizer for the traffic simulator using tkinter."""

import tkinter as tk
from typing import List

from town import Town, TrafficSimulator, Vehicle

CELL_SIZE = 40
VEHICLE_COLORS = ["red", "blue", "green", "purple", "orange"]


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
    town = Town(width=5, height=5)
    town.set_road_weight((1, 2), (2, 2), 5.0)
    town.set_road_weight((2, 2), (2, 3), 3.0)

    root = tk.Tk()
    root.title("Traffic Simulator")
    canvas = tk.Canvas(root, width=town.width * CELL_SIZE, height=town.height * CELL_SIZE)
    canvas.pack()

    draw_grid(canvas, town)

    simulator = VisualTrafficSimulator(town, canvas)
    simulator.add_vehicle(Vehicle(start=(0, 0), goal=(4, 4)))
    simulator.add_vehicle(Vehicle(start=(4, 0), goal=(0, 4)))

    def loop() -> None:
        if not simulator.is_complete():
            simulator.step()
            root.after(500, loop)
        else:
            print("Simulation complete.")

    root.after(500, loop)
    root.mainloop()


if __name__ == "__main__":
    main()
