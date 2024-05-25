# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wall following maze solver.
#
# **author** = 'Jeffrey Chan'
# **copyright** = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation. You'll need to complete its implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False

        # Define the order of directions for rotation
        directions = [
            Coordinates3D(0, -1, 0), # North
            Coordinates3D(1, 0, 0), # Up (North-East)
            Coordinates3D(0, 0, 1), # East
            Coordinates3D(0, 1, 0), # South
            Coordinates3D(-1, 0, 0), # Down (South-West)
            Coordinates3D(0, 0, -1) # West
        ]

        # Set the initial direction
        direction_index = 0

        # Set the current cell to the entrance
        current_cell = entrance

        # Initialize the path with the entrance cell
        self.solverPathAppend(current_cell, False)

        # Initialize a stack to store visited cells
        visited_cells = [current_cell]

        # Initialize a set to keep track of visited cells
        visited_cells_set = set(visited_cells)

        while current_cell not in maze.getExits():
            # Get the next cell in the current direction
            next_cell_row = current_cell.getRow() + directions[direction_index].getRow()
            next_cell_col = current_cell.getCol() + directions[direction_index].getCol()
            next_cell_level = current_cell.getLevel() + directions[direction_index].getLevel()

            # Create a Coordinates3D object for the next cell
            next_cell = Coordinates3D(next_cell_row, next_cell_col, next_cell_level)

            # Check if the next cell is within the maze boundaries and not a wall
            if maze.hasCell(next_cell) and not maze.hasWall(current_cell, next_cell):
                # Check if the next cell has already been visited
                if next_cell not in visited_cells_set:
                    # Move to the next cell
                    current_cell = next_cell
                    visited_cells.append(current_cell)
                    visited_cells_set.add(current_cell)
                    self.solverPathAppend(current_cell, False)
                else:
                    # Rotate to the next direction
                    direction_index = (direction_index + 1) % len(directions)
            else:
                # Rotate to the next direction
                direction_index = (direction_index + 1) % len(directions)

            # If all directions have been tried, backtrack
            if direction_index == 0:
                if len(visited_cells) > 1:
                    current_cell = visited_cells.pop()
                    visited_cells_set.remove(current_cell)
                    self.solverPathAppend(current_cell, True)
                else:
                    # No solution found and no more cells to backtrack to
                    self.m_solved = False
                    return

        # Check if we have found the exit
        if current_cell in maze.getExits():
            self.solved(entrance, current_cell)
