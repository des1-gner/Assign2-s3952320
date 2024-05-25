# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wilson's algorithm maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import choice
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """

    def generateMaze(self, maze: Maze3D):
        # Initialize the maze with all walls
        maze.initCells(True)

        # Create a set to store finalized cells
        finalized: set[Coordinates3D] = set()

        # Randomly select the first finalized cell
        startLevel = choice(range(maze.levelNum()))
        startRow = choice(range(maze.rowNum(startLevel)))
        startCol = choice(range(maze.colNum(startLevel)))
        startCoord: Coordinates3D = Coordinates3D(startLevel, startRow, startCol)
        finalized.add(startCoord)

        # Iterate until all cells are finalized
        while len(finalized) < sum(maze.rowNum(level) * maze.colNum(level) for level in range(maze.levelNum())):
            # Randomly select an unfinalized cell
            currLevel = choice(range(maze.levelNum()))
            currRow = choice(range(maze.rowNum(currLevel)))
            currCol = choice(range(maze.colNum(currLevel)))
            currCoord: Coordinates3D = Coordinates3D(currLevel, currRow, currCol)

            # Perform a random walk until a finalized cell is reached
            path: list[Coordinates3D] = [currCoord]
            while currCoord not in finalized:
                # Get the valid neighbors of the current cell
                neighbors: list[Coordinates3D] = [neigh for neigh in maze.neighbours(currCoord) if self.isValidCell(maze, neigh)]

                # Choose the next cell randomly from the valid neighbors
                nextCoord: Coordinates3D = choice(neighbors)

                # Remove the wall between the current cell and the next cell
                maze.removeWall(currCoord, nextCoord)

                # Update the current cell and add it to the path
                currCoord = nextCoord
                path.append(currCoord)

            # Add the cells in the path to the finalized set
            finalized.update(path)

        # Update maze generated flag
        self.m_mazeGenerated = True

    def isValidCell(self, maze: Maze3D, cell: Coordinates3D) -> bool:
        level, row, col = cell.getLevel(), cell.getRow(), cell.getCol()
        return 0 <= level < maze.levelNum() and 0 <= row < maze.rowNum(level) and 0 <= col < maze.colNum(level)
