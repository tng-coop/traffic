# Traffic Simulator

This repository contains a very small traffic simulator written in pure
Python. It uses the A* algorithm to plan routes across a grid-based town.
The code is intentionally simple so it can run in a restricted Codex
environment with no external dependencies. The GUI now draws roads as
gray rectangles with lane markings and includes simple traffic signal
visuals at each intersection. Recent updates add a yellow phase to the
signals and allow intersections to use independent random offsets so the
lights are no longer synchronized.

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
gray rectangles with dashed lane markings and each intersection has its own
red/yellow/green cycle. Signal phases are offset randomly across the town so
lights change at different times. Twenty vehicles are created with random
start and goal positions and move along their planned routes in real time,
waiting whenever the next intersection shows yellow or red.

## Using the library

The main logic lives in `town.py` and provides these classes:

- `Town`: manages intersections and road weights. It can generate either a
  regular grid or a random network with roads of varying length.
- `TrafficSimulator`: steps vehicles along their planned paths while
  updating traffic signals.
- `Vehicle`: stores start and goal positions and the computed path.

You can modify road weights with `Town.set_road_weight` to simulate traffic
conditions. Signals toggle automatically each simulation step using
`Town.update_signals`. Intersections can use independent signal phases with a
green/yellow/red cycle to better mimic real traffic lights.
