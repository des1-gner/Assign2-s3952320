# -------------------------------------------------------------------
# Implementation of Task D maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

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

