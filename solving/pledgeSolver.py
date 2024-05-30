from typing import List, Tuple
from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
import random

class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation for 3D mazes.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        directions = [
            Coordinates3D(0, 1, 0),   # South
            Coordinates3D(0, 0, 1),   # East
            Coordinates3D(0, -1, 0),  # North
            Coordinates3D(0, 0, -1),  # West
            Coordinates3D(1, 0, 0),   # Up (to next level)
            Coordinates3D(-1, 0, 0)   # Down (to previous level)
        ]

        current_cell = entrance
        current_direction_index = 0  # Start with a fixed direction (South)
        angle = 0
        visited = set()
        path = [current_cell]

        def is_within_bounds(cell):
            return maze.hasCell(cell)

        while True:
            if is_within_bounds(current_cell):
                visited.add(current_cell)
                self.solverPathAppend(current_cell, False)

            if current_cell in maze.getExits():
                self.solverPathAppend(current_cell, True)
                break

            next_cell = current_cell + directions[current_direction_index]

            if is_within_bounds(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                current_cell = next_cell
                path.append(current_cell)
                visited.add(current_cell)
                self.solverPathAppend(current_cell, False)
                angle = 0  # Reset angle when a valid move is found
            else:
                found_path = False
                for _ in range(len(directions)):
                    current_direction_index = (current_direction_index + 1) % len(directions)
                    next_cell = current_cell + directions[current_direction_index]

                    if is_within_bounds(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                        current_cell = next_cell
                        path.append(current_cell)
                        visited.add(current_cell)
                        self.solverPathAppend(current_cell, False)
                        found_path = True
                        break

                if not found_path:
                    if len(path) > 1:
                        path.pop()
                        current_cell = path[-1]
                    else:
                        self.m_solved = False
                        return

        self.solved(entrance, current_cell)

