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
from typing import Dict, List, Optional, Tuple


@dataclass
class Node:
    """A node in the grid representing an intersection."""

    x: int
    y: int
    neighbors: Dict[Tuple[int, int], float] = field(default_factory=dict)


class Town:
    """Grid-based town with roads connecting intersections."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.nodes: Dict[Tuple[int, int], Node] = {}
        self._create_grid()

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

    def set_road_weight(self, a: Tuple[int, int], b: Tuple[int, int], weight: float) -> None:
        """Set weight for the road between two intersections."""
        if b in self.nodes[a].neighbors:
            self.nodes[a].neighbors[b] = weight
            self.nodes[b].neighbors[a] = weight

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

    def move(self) -> Optional[Tuple[int, int]]:
        """Move the vehicle along its path by one step."""
        if self.position_index < len(self.path) - 1:
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
        for vehicle in self.vehicles:
            vehicle.move()

    def is_complete(self) -> bool:
        return all(v.position_index >= len(v.path) - 1 for v in self.vehicles)

