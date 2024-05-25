# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Pledge maze solver.
#
# **author** = 'Jeffrey Chan'
# **copyright** = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
import random

class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation. You'll need to complete its implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False

        # Define the order of directions for rotation
        directions = [
            Coordinates3D(0, -1, 0),  # North
            Coordinates3D(1, 0, 0),  # Up (North-East)
            Coordinates3D(0, 0, 1),  # East
            Coordinates3D(0, 1, 0),  # South
            Coordinates3D(-1, 0, 0),  # Down (South-West)
            Coordinates3D(0, 0, -1)  # West
        ]

        # Set the initial direction randomly
        initial_direction_index = random.randint(0, len(directions) - 1)
        direction_index = initial_direction_index

        # Set the current cell to the entrance
        current_cell = entrance

        # Initialize the path with the entrance cell
        self.solverPathAppend(current_cell, False)

        # Initialize a stack to store visited cells
        visited_cells = [current_cell]

        # Initialize a set to keep track of visited cells during wall-following
        wall_following_visited_set = set()

        # Initialize a set to keep track of visited cells during initial direction
        initial_direction_visited_set = set([current_cell])

        # Initialize the angle of turns
        angle = 0

        while True:
            # Get the next cell in the current direction
            next_cell_row = current_cell.getRow() + directions[direction_index].getRow()
            next_cell_col = current_cell.getCol() + directions[direction_index].getCol()
            next_cell_level = current_cell.getLevel() + directions[direction_index].getLevel()

            # Create a Coordinates3D object for the next cell
            next_cell = Coordinates3D(next_cell_row, next_cell_col, next_cell_level)

            # Check if the next cell is within the maze boundaries
            if maze.hasCell(next_cell):
                # Check if the next cell is not a wall
                if not maze.hasWall(current_cell, next_cell):
                    # Check if the next cell has already been visited
                    if next_cell not in wall_following_visited_set and next_cell not in initial_direction_visited_set:
                        # Move to the next cell
                        current_cell = next_cell
                        visited_cells.append(current_cell)

                        # If we're in the initial direction mode
                        if angle % 360 == 0:
                            initial_direction_visited_set.add(current_cell)
                        else:
                            wall_following_visited_set.add(current_cell)

                        self.solverPathAppend(current_cell, False)

                        # Check if we have found the exit
                        if current_cell in maze.getExits():
                            self.m_solved = True
                            return
                    else:
                        # Rotate to the next direction
                        old_direction_index = direction_index
                        direction_index = (direction_index + 1) % len(directions)

                        # Update the angle based on the turn
                        if direction_index == (old_direction_index + 1) % len(directions):
                            angle += 60
                        else:
                            angle -= 60

                        # If we've rotated back to the initial direction (angle = 0)
                        if angle % 360 == 0:
                            direction_index = initial_direction_index
                            initial_direction_visited_set.clear()
                            initial_direction_visited_set.add(current_cell)
                else:
                    # Rotate to the next direction
                    old_direction_index = direction_index
                    direction_index = (direction_index + 1) % len(directions)

                    # Update the angle based on the turn
                    if direction_index == (old_direction_index + 1) % len(directions):
                        angle += 60
                    else:
                        angle -= 60
            else:
                # Rotate to the next direction
                direction_index = (direction_index + 1) % len(directions)

            # If all directions have been tried, backtrack
            if direction_index == 0:
                if len(visited_cells) > 1:
                    current_cell = visited_cells.pop()
                    try:
                        if angle % 360 == 0:
                            initial_direction_visited_set.remove(current_cell)
                        else:
                            wall_following_visited_set.remove(current_cell)
                    except KeyError:
                        # Handle the case when the element is not present in the set
                        pass
                    self.solverPathAppend(current_cell, True)
                else:
                    # We've exhausted all possibilities, but no solution found
                    self.m_solved = False
                    return
