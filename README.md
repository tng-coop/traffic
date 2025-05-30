# Traffic Simulator

This repository contains a very small traffic simulator written in pure
Python. It uses the A* algorithm to plan routes across a grid-based town.
The code is intentionally simple so it can run in a restricted Codex
environment with no external dependencies. The GUI now draws roads as
gray rectangles with lane markings and includes simple traffic signal
visuals at each intersection.

## Running the example

To try the simulator run:

```bash
python run_simulation.py
```

This prints an ASCII representation of the town at each step. A simple
animated GUI version using `tkinter` is also available:

```bash
python run_simulation_gui.py
```

This will open a window showing a 10x10 town. Roads are displayed using
gray rectangles with dashed lane markings and each intersection has a
traffic signal that toggles between red and green. Twenty vehicles are
created with random start and goal positions and move along their planned
routes in real time, waiting at red lights.

## Using the library

The main logic lives in `town.py` and provides these classes:

- `Town`: manages a grid of intersections and road weights.
- `TrafficSimulator`: steps vehicles along their planned paths while
  updating traffic signals.
- `Vehicle`: stores start and goal positions and the computed path.

You can modify road weights with `Town.set_road_weight` to simulate traffic
conditions. Signals toggle automatically each simulation step using
`Town.update_signals`.
