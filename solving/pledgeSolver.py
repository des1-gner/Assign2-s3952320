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

        print(f"Starting at entrance: {entrance}")
        print(f"Initial direction: {directions[current_direction_index]}")

        def is_within_bounds(cell):
            return maze.hasCell(cell)

        while True:
            # Ensure the current cell is within the maze dimensions before marking
            if is_within_bounds(current_cell):
                visited.add(current_cell)
                self.solverPathAppend(current_cell, False)

            if current_cell in maze.getExits():
                self.solverPathAppend(current_cell, True)
                print(f"Exit found at: {current_cell}")
                break

            while True:
                next_cell = current_cell + directions[current_direction_index]
                print(f"Trying to move from {current_cell} to {next_cell}")

                if is_within_bounds(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                    current_cell = next_cell
                    path.append(current_cell)
                    if is_within_bounds(current_cell):  # Ensure the next cell is within the maze dimensions before marking
                        visited.add(current_cell)
                        self.solverPathAppend(current_cell, False)
                    print(f"Moved to {current_cell}")
                    if current_cell in maze.getExits():
                        self.solverPathAppend(current_cell, True)
                        print(f"Exit found at: {current_cell}")
                        return
                else:
                    print(f"Hit a wall or visited cell at {next_cell}")
                    break

            found_path = False
            while not found_path:
                for _ in range(len(directions)):
                    next_cell = current_cell + directions[current_direction_index]
                    print(f"Wall-following: trying to move from {current_cell} to {next_cell}")

                    if is_within_bounds(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                        current_cell = next_cell
                        path.append(current_cell)
                        if is_within_bounds(current_cell):  # Ensure the next cell is within the maze dimensions before marking
                            visited.add(current_cell)
                            self.solverPathAppend(current_cell, False)
                        found_path = True
                        print(f"Wall-following: moved to {current_cell}")
                        break
                    else:
                        old_direction_index = current_direction_index
                        current_direction_index = (current_direction_index + 1) % len(directions)
                        if current_direction_index == (old_direction_index + 1) % len(directions):
                            angle += 60
                        else:
                            angle -= 60
                        print(f"Turning: new direction {directions[current_direction_index]}, angle {angle}")

                if angle == 0:
                    current_direction_index = initial_direction_index
                    print(f"Angle is zero, reverting to initial direction: {directions[initial_direction_index]}")
                    break

                if not found_path and len(path) > 1:
                    current_cell = path[-2]
                    path.pop()
                    print(f"Backtracking to {current_cell}")

            if not found_path and len(path) <= 1:
                self.m_solved = False
                print("No solution found, exiting")
                return

        self.solved(entrance, current_cell)

