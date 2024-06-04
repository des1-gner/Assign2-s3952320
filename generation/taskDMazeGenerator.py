# -------------------------------------------------------------------
# Implementation of Task D maze generator.
#
# __author__ = 'Jeffrey Chan', 'Oisin Aeonn'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

# Import Libraries

from random import choice
from collections import deque

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator


class TaskDMazeGenerator(MazeGenerator):
    """
    Implementation of Task D: Maximising Solver Exploration of Cells
    """

    def generateMaze(self, maze: Maze3D):
        # Initialize maze with all walls
        maze.initCells(True)

        # Define entrances and exits from the provided example
        entrance1 = Coordinates3D(0, 0, -1)  # Entrance 1
        entrance2 = Coordinates3D(1, -1, 1)  # Entrance 2
        exits = [Coordinates3D(0, 5, 1)]     # Exit

        # Start from the first entrance for the longest path
        startCoord = entrance1

        # Initialize stack and visited set
        stack = deque()
        stack.append(startCoord)
        visited = set([startCoord])

        # Use DFS to create a single path from entrance to exit
        currCell = startCoord
        path = []

        while stack:
            path.append(currCell)
            neighbours = maze.neighbours(currCell)
            nonVisitedNeighs = [neigh for neigh in neighbours if neigh not in visited and
                                0 <= neigh.getRow() < maze.rowNum(neigh.getLevel()) and
                                0 <= neigh.getCol() < maze.colNum(neigh.getLevel())]
            if nonVisitedNeighs:
                neigh = choice(nonVisitedNeighs)
                maze.removeWall(currCell, neigh)
                stack.append(neigh)
                visited.add(neigh)
                currCell = neigh
            else:
                currCell = stack.pop()

            if currCell in exits:
                break

        # Create a single path maze
        self.createSinglePath(maze, path, visited)

        # Fill in the rest of the maze
        self.fillMaze(maze, visited)

        # Ensure boundaries are intact
        self.fixBoundaries(maze)

        # Update maze generated
        self.m_mazeGenerated = True

    def createSinglePath(self, maze, path, visited):
        for i in range(len(path) - 1):
            currCell = path[i]
            nextCell = path[i + 1]
            if nextCell not in visited:
                maze.removeWall(currCell, nextCell)
                visited.add(nextCell)

    def fillMaze(self, maze, visited):
        stack = deque(visited)
        totalCells = sum([maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum())])

        while len(visited) < totalCells:
            if not stack:
                break

            currCell = stack.pop()
            neighbours = maze.neighbours(currCell)
            nonVisitedNeighs = [neigh for neigh in neighbours if neigh not in visited and
                                0 <= neigh.getRow() < maze.rowNum(neigh.getLevel()) and
                                0 <= neigh.getCol() < maze.colNum(neigh.getLevel())]
            if nonVisitedNeighs:
                neigh = choice(nonVisitedNeighs)
                maze.removeWall(currCell, neigh)
                stack.append(neigh)
                visited.add(neigh)

    def fixBoundaries(self, maze):
        for level in range(maze.levelNum()):
            for row in range(maze.rowNum(level)):
                for col in range(maze.colNum(level)):
                    cell = Coordinates3D(level, row, col)
                    if cell not in [Coordinates3D(0, 0, -1), Coordinates3D(1, -1, 1), Coordinates3D(0, 5, 1)]:
                        if row == 0:
                            maze.addWall(cell, Coordinates3D(level, row - 1, col))
                        if row == maze.rowNum(level) - 1:
                            maze.addWall(cell, Coordinates3D(level, row + 1, col))
                        if col == 0:
                            maze.addWall(cell, Coordinates3D(level, row, col - 1))
                        if col == maze.colNum(level) - 1:
                            maze.addWall(cell, Coordinates3D(level, row, col + 1))

