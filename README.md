# Traffic Simulator

This repository contains a very small traffic simulator written in pure
Python. It uses the A* algorithm to plan routes across a grid-based town.
The code is intentionally simple so it can run in a restricted Codex
environment with no external dependencies.

## Running the example

To try the simulator run:

```bash
python run_simulation.py
```

This will create a small 5x5 town grid, add two vehicles, and step them
through the town while printing their positions.

## Using the library

The main logic lives in `town.py` and provides these classes:

- `Town`: manages a grid of intersections and road weights.
- `TrafficSimulator`: steps vehicles along their planned paths.
- `Vehicle`: stores start and goal positions and the computed path.

You can modify road weights with `Town.set_road_weight` to simulate traffic
conditions.
