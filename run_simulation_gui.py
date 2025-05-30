"""GUI visualizer for the traffic simulator using tkinter.

This version creates a 10x10 town and spawns 20 vehicles with random
start and end points. Roads are drawn as gray rectangles with lane
markings and intersections display traffic signal lights. Each vehicle is
represented as a colored circle moving along its planned path.
"""

import tkinter as tk
import random
from typing import Dict, List

from town import Town, TrafficSimulator, Vehicle

CELL_SIZE = 40
ROAD_WIDTH = 8
VEHICLE_RADIUS = 6
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

    def __init__(self, town: Town, canvas: tk.Canvas, signal_items: Dict[tuple[int, int], int]) -> None:
        super().__init__(town)
        self.canvas = canvas
        self.vehicle_items: List[int] = []
        self.signal_items = signal_items

    def add_vehicle(self, vehicle: Vehicle) -> None:
        super().add_vehicle(vehicle)
        # Create a circle to represent this vehicle at the intersection center
        color = VEHICLE_COLORS[len(self.vehicle_items) % len(VEHICLE_COLORS)]
        if vehicle.path:
            x, y = vehicle.path[0]
        else:
            x, y = vehicle.start
        cx = x * CELL_SIZE + CELL_SIZE / 2
        cy = y * CELL_SIZE + CELL_SIZE / 2
        item = self.canvas.create_oval(
            cx - VEHICLE_RADIUS,
            cy - VEHICLE_RADIUS,
            cx + VEHICLE_RADIUS,
            cy + VEHICLE_RADIUS,
            fill=color,
            outline=""
        )
        self.vehicle_items.append(item)

    def step(self) -> None:
        super().step()
        for (x, y), item in self.signal_items.items():
            sig = self.town.nodes[(x, y)].signal
            color = {"green": "green", "yellow": "yellow", "red": "red"}[sig]
            self.canvas.itemconfig(item, fill=color)
        for vehicle, item in zip(self.vehicles, self.vehicle_items):
            x, y = vehicle.path[vehicle.position_index]
            cx = x * CELL_SIZE + CELL_SIZE / 2
            cy = y * CELL_SIZE + CELL_SIZE / 2
            self.canvas.coords(
                item,
                cx - VEHICLE_RADIUS,
                cy - VEHICLE_RADIUS,
                cx + VEHICLE_RADIUS,
                cy + VEHICLE_RADIUS,
            )


def draw_roads(canvas: tk.Canvas, town: Town) -> Dict[tuple[int, int], int]:
    """Draw road rectangles and traffic signals."""

    def center(pt: tuple[int, int]) -> tuple[float, float]:
        x, y = pt
        return x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2

    # draw road segments
    for (x, y), node in town.nodes.items():
        cx, cy = center((x, y))
        for nx, ny in node.neighbors:
            if (nx, ny) < (x, y):
                continue  # avoid drawing the same road twice
            ncx, ncy = center((nx, ny))
            if x == nx or y == ny:
                # horizontal or vertical road with lane markings
                if x == nx:
                    x1 = cx - ROAD_WIDTH / 2
                    x2 = cx + ROAD_WIDTH / 2
                    y1, y2 = sorted([cy, ncy])
                    canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="")
                    canvas.create_line(cx, y1, cx, y2, fill="white", dash=(4, 4))
                else:
                    y1 = cy - ROAD_WIDTH / 2
                    y2 = cy + ROAD_WIDTH / 2
                    x1, x2 = sorted([cx, ncx])
                    canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="")
                    canvas.create_line(x1, cy, x2, cy, fill="white", dash=(4, 4))
            else:
                # diagonal road drawn as a simple thick line
                canvas.create_line(
                    cx,
                    cy,
                    ncx,
                    ncy,
                    fill="gray",
                    width=ROAD_WIDTH,
                )

    signal_items: Dict[tuple[int, int], int] = {}
    for (x, y) in town.nodes:
        cx, cy = center((x, y))
        r = ROAD_WIDTH / 2
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="black")
        sig = town.nodes[(x, y)].signal
        color = {"green": "green", "yellow": "yellow", "red": "red"}[sig]
        signal_items[(x, y)] = canvas.create_oval(
            cx - r / 2,
            cy - r / 2,
            cx + r / 2,
            cy + r / 2,
            fill=color,
            outline="",
        )
    return signal_items


def main() -> None:
    # Create a town with random roads and signal offsets
    town = Town(
        width=10,
        height=10,
        randomize_signals=True,
        random_roads=True,
    )

    root = tk.Tk()
    root.title("Traffic Simulator")
    canvas = tk.Canvas(root, width=town.width * CELL_SIZE, height=town.height * CELL_SIZE)
    canvas.pack()

    signal_items = draw_roads(canvas, town)

    simulator = VisualTrafficSimulator(town, canvas, signal_items)
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
