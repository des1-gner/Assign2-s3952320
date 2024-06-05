# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wall following maze solver.
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

    # Function to get coordinate, though can be done with .value
    def getValue(self) -> Coordinates3D:
        """
        Gets Coordinates3D value of direction
        """
        return self.value

    # Functions to get the next direction
    def getRight(self):
        """
        Gets the right direction of a current value according to the order of enums
        """
        directions = list(Directions)
        current_index = directions.index(self)
        next_index = (current_index + 1) % len(
            directions
        )  # Cycle to the beginning if at the end
        return directions[next_index]

    def getLeft(self):
        """
        Gets the left direction of a current value according to the order of enums
        """
        directions = list(Directions)
        current_index = directions.index(self)
        next_index = (current_index - 1) % len(
            directions
        )  # Cycle to the beginning if at the end
        return directions[next_index]

    # Function to get the opposite direction
    def getOppositeDirection(self):
        """
        Get the opposite direction of the current direction,
        which is currently 3 rotations to the left or right
        """
        directions = list(Directions)
        current_index = directions.index(self)
        next_index = (current_index + 3) % len(
            directions
        )  # Cycle to the beginning if at the end
        return directions[next_index]

    # Function used to get the direction after entering a boundary space
    def getDirection(self, srcCell, destCell):
        """
        Return direction enum between based on a source cell and destination cell that are adjacent
        """
        # direction found by finding the difference between destination cell and current cell.
        destinationDirection = Coordinates3D(
            destCell.getLevel() - srcCell.getLevel(),
            destCell.getRow() - srcCell.getRow(),
            destCell.getCol() - srcCell.getCol(),
        )
        for direction in Directions:
            if direction.value == destinationDirection:
                return direction
        return None


class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation.  You'll need to complete its implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        startCoord: Coordinates3D = entrance

        # Set beginning direction
        BEGINNING_DIRECTION: Directions = Directions.NORTH

        # currCell is startCoord
        currCell: Coordinates3D = startCoord
        # Beginning direction of algorithm
        currDirection: Directions = BEGINNING_DIRECTION

        # Use a set to store unique cells
        visitedCells = set()

        # Begin algorithm
        while currCell not in maze.getExits():
            # append cell visited by algorithm
            if currCell not in visitedCells:
                self.solverPathAppend(currCell)
                visitedCells.add(currCell)

            # Get list of neighbours
            neighbours: list[Coordinates3D] = maze.neighbours(currCell)

            # Neighbours that can be visited (non-walls)
            possibleNeighs: list[Coordinates3D] = [
                neigh
                for neigh in neighbours
                if not maze.hasWall(currCell, neigh)
                and (neigh.getRow() >= -1)
                and (neigh.getRow() <= maze.rowNum(neigh.getLevel()))
                and (neigh.getCol() >= -1)
                and (neigh.getCol() <= maze.colNum(neigh.getLevel()))
            ]
            # Get opposite direction (which cell you came from)
            currDirection = currDirection.getOppositeDirection()

            # Check wall one rotation to the right, change this to change which wall to follow
            currDirection = currDirection.getLeft()
            # While cannot move forward
            while (currCell + currDirection.getValue()) not in possibleNeighs:
                # Check wall one rotation to the right, change this to change which wall to follow
                currDirection = currDirection.getLeft()

            # Move forward if there is no wall
            currCell = currCell + currDirection.getValue()

        # ensure we are currently at the exit
        if currCell in maze.getExits():
            # append exit cell to solverPath
            self.solverPathAppend(currCell)
            self.solved(entrance, currCell)

        # Assign unique visited cells to the explored cells metric
        self.m_exploredCells = len(visitedCells)

