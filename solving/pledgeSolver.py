from typing import List, Tuple
from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
import random


class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False

        # Define directions: North, Up (North-East), East, South, Down (South-West), West
        directions = [
            Coordinates3D(0, 1, 0),   # North
            Coordinates3D(0, 0, 1),   # Up
            Coordinates3D(1, 0, 0),   # East
            Coordinates3D(0, -1, 0),  # South
            Coordinates3D(0, 0, -1),  # Down
            Coordinates3D(-1, 0, 0)   # West
        ]

        # Choose initial direction randomly
        initial_direction_index = random.randint(0, len(directions) - 1)
        direction_index = initial_direction_index
        angle = 0
        current_cell = entrance

        # Set to track visited cells
        visited_cells = set()
        visited_cells.add(current_cell)

        self.solverPathAppend(current_cell, False)

        while True:
            if current_cell in maze.getExits():
                self.m_solved = True
                self.solved(entrance, current_cell)
                return

            # Attempt to move in the current direction until hitting a wall or finding the exit
            while True:
                next_cell = Coordinates3D(
                    current_cell.getRow() + directions[direction_index].getRow(),
                    current_cell.getCol() + directions[direction_index].getCol(),
                    current_cell.getLevel() + directions[direction_index].getLevel()
                )

                if maze.hasCell(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited_cells:
                    # Move to the next cell
                    current_cell = next_cell
                    self.solverPathAppend(current_cell, False)
                    visited_cells.add(current_cell)
                    if current_cell in maze.getExits():
                        self.m_solved = True
                        self.solved(entrance, current_cell)
                        return
                else:
                    # Start wall-following
                    while True:
                        old_direction_index = direction_index
                        direction_index = (direction_index + 1) % len(directions)
                        angle += 60 if direction_index == (old_direction_index + 1) % len(directions) else -60

                        next_cell = Coordinates3D(
                            current_cell.getRow() + directions[direction_index].getRow(),
                            current_cell.getCol() + directions[direction_index].getCol(),
                            current_cell.getLevel() + directions[direction_index].getLevel()
                        )

                        if angle == 0:
                            break

                        # Check if we can move to the next cell
                        if maze.hasCell(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited_cells:
                            current_cell = next_cell
                            self.solverPathAppend(current_cell, False)
                            visited_cells.add(current_cell)
                            break
                        else:
                            # If we can't move, check if there's a previous cell to backtrack to
                            if len(self.m_solverPath) > 1:
                                self.solverPathAppend(current_cell, True)
                                current_cell = self.m_solverPath[-2][0]  # Backtrack
                                visited_cells.add(current_cell)
                            else:
                                # No solution found
                                self.m_solved = False
                                return

                    # Restore initial direction when angle is zero
                    if angle == 0:
                        direction_index = initial_direction_index
                        break

