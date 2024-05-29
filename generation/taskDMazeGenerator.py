# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
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

        # Define entrance and exit
        entrance = Coordinates3D(0, 0, 0)  # Assuming entrance at level 0, row 0, column 0
        exit_level = maze.levelNum() - 1
        exit_row = maze.rowNum(exit_level) - 1
        exit_col = maze.colNum(exit_level) - 1
        exit = Coordinates3D(exit_level, exit_row, exit_col)

        # Initialize stack and visited set
        stack = deque()
        stack.append(entrance)
        visited = set([entrance])

        # Use DFS to create a single path from entrance to exit
        currCell = entrance
        path = []

        while currCell != exit:
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

