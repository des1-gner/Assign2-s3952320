# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Prim's maze generator.
#
# __author__ = 'Jeffrey Chan', 'Oisin Aeonn'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

# Imported Libraries

from random import randint, choice

class PrimMazeGenerator(MazeGenerator):

    """
    Prim's algorithm maze generator.
    TODO: Complete the implementation (Task A)
    Done :)
    """

    # Generates a maze using Prim's algorithm

    def generateMaze(self, maze: Maze3D):
        
        # Initialize the maze with all walls
        
        maze.initCells(True)

        # Select a random starting cell
        
        startLevel = randint(0, maze.levelNum() - 1)
        startCoord: Coordinates3D = Coordinates3D(startLevel, randint(0, maze.rowNum(startLevel) - 1),
                                                  randint(0, maze.colNum(startLevel) - 1))

        # Create a set to store visited cells
        
        visited: set[Coordinates3D] = set([startCoord])

        # Create a list to store the frontier cells
        
        frontier: list[Coordinates3D] = []

        # Add the neighbors of the starting cell to the frontier
        
        for neigh in maze.neighbours(startCoord):
        
            if self.isValidCell(maze, neigh):
        
                frontier.append(neigh)

        while frontier:
        
            # Randomly select a cell from the frontier
        
            currCell: Coordinates3D = choice(frontier)

            # Find the visited neighbors of the current cell
        
            visitedNeighs: list[Coordinates3D] = [neigh for neigh in maze.neighbours(currCell) if neigh in visited]

            # If there are visited neighbors
        
            if visitedNeighs:
        
                # Randomly select a visited neighbor
        
                neigh = choice(visitedNeighs)

                # Remove the wall between the current cell and the selected neighbor
        
                maze.removeWall(currCell, neigh)

                # Add the current cell to the visited set
        
                visited.add(currCell)

            # Remove the current cell from the frontier
        
            frontier.remove(currCell)

            # Add the unvisited neighbors of the current cell to the frontier
        
            for neigh in maze.neighbours(currCell):
        
                if neigh not in visited and neigh not in frontier and self.isValidCell(maze, neigh):
        
                    frontier.append(neigh)

        # Update maze generated flag
        
        self.m_mazeGenerated = True

    # Checks if a cell is within the bounds of the maze

    def isValidCell(self, maze: Maze3D, cell: Coordinates3D) -> bool:
        
        level, row, col = cell.getLevel(), cell.getRow(), cell.getCol()
        
        # True if the cell is within the maze bounds, False otherwise
        
        return 0 <= level < maze.levelNum() and 0 <= row < maze.rowNum(level) and 0 <= col < maze.colNum(level)
