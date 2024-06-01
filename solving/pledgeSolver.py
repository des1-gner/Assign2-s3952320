# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Pledge maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from enum import Enum

class Directions(Enum):
    """
    Convention is (level, row, col) for constructing 3D Coordinates
    Enums for level, row, and col
    Has directions: North, North-East, East, South, South-West, West
    """
    NORTH = Coordinates3D(0, 1, 0)
    NORTH_EAST = Coordinates3D(1, 0, 0)  # Up
    EAST = Coordinates3D(0, 0, 1)
    SOUTH = Coordinates3D(0, -1, 0)
    SOUTH_WEST = Coordinates3D(-1, 0, 0)  # Down
    WEST = Coordinates3D(0, 0, -1)

    def getValue(self) -> Coordinates3D:
        """
        Gets Coordinates3D value of direction
        """
        return self.value

    def getRight(self):
        """
        Gets the right direction of a current value according to the order of enums
        """
        directions = list(Directions)
        current_index = directions.index(self)
        next_index = (current_index + 1) % len(directions)  # Cycle to the beginning if at the end
        return directions[next_index]

    def getLeft(self):
        """
        Gets the left direction of a current value according to the order of enums
        """
        directions = list(Directions)
        current_index = directions.index(self)
        next_index = (current_index - 1) % len(directions)  # Cycle to the beginning if at the end
        return directions[next_index]

    def getOppositeDirection(self):
        """
        Get the opposite direction of the current direction,
        which is currently 3 rotations to the left or right
        """
        directions = list(Directions)
        current_index = directions.index(self)
        next_index = (current_index + 3) % len(directions)  # Cycle to the beginning if at the end
        return directions[next_index]

    def getDirection(self, srcCell, destCell):
        """
        Return direction enum based on a source cell and destination cell that are adjacent
        """
        destinationDirection = Coordinates3D(
            destCell.getLevel() - srcCell.getLevel(),
            destCell.getRow() - srcCell.getRow(),
            destCell.getCol() - srcCell.getCol(),
        )
        for direction in Directions:
            if direction.value == destinationDirection:
                return direction
        return None

class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation for 3D mazes.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        directions = [
            Coordinates3D(0, 1, 0),   # North
            Coordinates3D(0, 0, 1),   # East
            Coordinates3D(0, -1, 0),  # South
            Coordinates3D(0, 0, -1),  # West
            Coordinates3D(1, 0, 0),   # Up (to next level)
            Coordinates3D(-1, 0, 0)   # Down (to previous level)
        ]

        current_cell = entrance
        current_direction_index = 0  # Start with a fixed direction (North)
        angle = 0
        visited = set()
        path = [current_cell]

        def is_within_bounds(cell):
            return maze.hasCell(cell)

        def is_valid_move(current, next_cell):
            return is_within_bounds(next_cell) and not maze.hasWall(current, next_cell) and next_cell not in visited and next_cell not in maze.getEntrances()

        while True:
            if is_within_bounds(current_cell):
                visited.add(current_cell)
                self.solverPathAppend(current_cell, False)

            if current_cell in maze.getExits():
                self.solverPathAppend(current_cell, True)
                break

            next_cell = current_cell + directions[current_direction_index]

            if is_valid_move(current_cell, next_cell):
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
                    angle += 90  # Turn right by 90 degrees

                    if angle == 360:
                        angle = 0

                    if is_valid_move(current_cell, next_cell):
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

