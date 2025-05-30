"""Simple A* based traffic simulation for a grid town.

The town is represented as a grid of intersections with roads
between adjacent intersections. Road weights represent travel time
and can be adjusted to simulate traffic.

This module is kept intentionally simple so it can run in restricted
Codex environments with no external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
import random
from typing import Dict, List, Optional, Tuple


@dataclass
class Node:
    """A node in the grid representing an intersection."""

    x: int
    y: int
    neighbors: Dict[Tuple[int, int], float] = field(default_factory=dict)
    signal: str = "green"
    signal_offset: int = 0


class Town:
    """Grid-based town with roads connecting intersections."""

    def __init__(
        self,
        width: int,
        height: int,
        signal_duration: int = 2,
        yellow_duration: int = 1,
        randomize_signals: bool = False,
        random_roads: bool = False,
    ) -> None:
        self.width = width
        self.height = height
        self.nodes: Dict[Tuple[int, int], Node] = {}
        self._create_grid() if not random_roads else self._create_random_roads()
        self.green_duration = signal_duration
        self.yellow_duration = yellow_duration
        self.red_duration = signal_duration
        self.randomize_signals = randomize_signals
        cycle = self.green_duration + self.yellow_duration + self.red_duration
        # Start so first update puts signals in red phase
        self.signal_step = self.green_duration + self.yellow_duration - 1
        for node in self.nodes.values():
            if randomize_signals:
                node.signal_offset = random.randint(0, cycle - 1)
            phase = (self.signal_step + node.signal_offset) % cycle
            node.signal = self._phase_to_color(phase)

    def _create_grid(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.nodes[(x, y)] = Node(x, y)

        # Connect nodes with unit cost roads by default
        for x in range(self.width):
            for y in range(self.height):
                node = self.nodes[(x, y)]
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        node.neighbors[(nx, ny)] = 1.0

    def _create_random_roads(self) -> None:
        """Create random road connections with varying lengths."""
        for x in range(self.width):
            for y in range(self.height):
                self.nodes[(x, y)] = Node(x, y)

        coords = list(self.nodes.keys())
        for a in coords:
            # each node connects to a few random other nodes
            choices = random.sample(coords, random.randint(2, 4))
            for b in choices:
                if a == b:
                    continue
                dist = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
                self.nodes[a].neighbors[b] = dist
                self.nodes[b].neighbors[a] = dist

    def set_road_weight(self, a: Tuple[int, int], b: Tuple[int, int], weight: float) -> None:
        """Set weight for the road between two intersections."""
        if b in self.nodes[a].neighbors:
            self.nodes[a].neighbors[b] = weight
            self.nodes[b].neighbors[a] = weight

    def _phase_to_color(self, phase: int) -> str:
        if phase < self.green_duration:
            return "green"
        if phase < self.green_duration + self.yellow_duration:
            return "yellow"
        return "red"

    def update_signals(self) -> None:
        """Update traffic signals using a green/yellow/red cycle."""
        self.signal_step += 1
        cycle = self.green_duration + self.yellow_duration + self.red_duration
        for node in self.nodes.values():
            phase = (self.signal_step + node.signal_offset) % cycle
            node.signal = self._phase_to_color(phase)

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Manhattan distance heuristic used for A* search."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """Return shortest path from start to goal using A* algorithm."""
        open_set: List[Tuple[float, Tuple[int, int]]] = []
        heappush(open_set, (0, start))

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score = {node: float("inf") for node in self.nodes}
        g_score[start] = 0
        f_score = {node: float("inf") for node in self.nodes}
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current = heappop(open_set)
            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbor, weight in self.nodes[current].neighbors.items():
                tentative_g_score = g_score[current] + weight
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if (f_score[neighbor], neighbor) not in open_set:
                        heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def _reconstruct_path(
        self, came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


@dataclass
class Vehicle:
    """Represents a vehicle moving through the town."""

    start: Tuple[int, int]
    goal: Tuple[int, int]
    path: List[Tuple[int, int]] = field(default_factory=list)
    position_index: int = 0

    def move(self, town: Town) -> Optional[Tuple[int, int]]:
        """Move the vehicle along its path by one step respecting signals."""
        if self.position_index < len(self.path) - 1:
            next_pos = self.path[self.position_index + 1]
            if town.nodes[next_pos].signal in ("red", "yellow"):
                return self.path[self.position_index]
            self.position_index += 1
            return self.path[self.position_index]
        return None


class TrafficSimulator:
    """Simple simulator that plans and steps vehicles through the town."""

    def __init__(self, town: Town) -> None:
        self.town = town
        self.vehicles: List[Vehicle] = []

    def add_vehicle(self, vehicle: Vehicle) -> None:
        vehicle.path = self.town.a_star(vehicle.start, vehicle.goal) or []
        self.vehicles.append(vehicle)

    def step(self) -> None:
        self.town.update_signals()
        for vehicle in self.vehicles:
            vehicle.move(self.town)

    def is_complete(self) -> bool:
        return all(v.position_index >= len(v.path) - 1 for v in self.vehicles)

