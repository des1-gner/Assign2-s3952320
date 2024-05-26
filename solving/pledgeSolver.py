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
        initial_direction_index = random.randint(0, len(directions) - 1)
        current_direction_index = initial_direction_index
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

            while True:
                next_cell = current_cell + directions[current_direction_index]

                if is_within_bounds(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                    current_cell = next_cell
                    path.append(current_cell)
                    if is_within_bounds(current_cell):
                        visited.add(current_cell)
                        self.solverPathAppend(current_cell, False)
                    if current_cell in maze.getExits():
                        self.solverPathAppend(current_cell, True)
                        return
                else:
                    break

            found_path = False
            while not found_path:
                for _ in range(len(directions)):
                    next_cell = current_cell + directions[current_direction_index]

                    if is_within_bounds(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                        current_cell = next_cell
                        path.append(current_cell)
                        if is_within_bounds(current_cell):
                            visited.add(current_cell)
                            self.solverPathAppend(current_cell, False)
                        found_path = True
                        break
                    else:
                        old_direction_index = current_direction_index
                        current_direction_index = (current_direction_index + 1) % len(directions)
                        if current_direction_index == (old_direction_index + 1) % len(directions):
                            angle += 60
                        else:
                            angle -= 60

                if angle == 0:
                    current_direction_index = initial_direction_index
                    break

                if not found_path and len(path) > 1:
                    current_cell = path[-2]
                    path.pop()

            if not found_path and len(path) <= 1:
                self.m_solved = False
                return

        self.solved(entrance, current_cell)

