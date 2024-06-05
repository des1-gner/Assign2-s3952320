from random import choice, shuffle
from collections import deque
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

class TaskDMazeGenerator(MazeGenerator):
    """
    Implementation of Task D: Maximising Solver Exploration of Cells
    """

    def generateMaze(self, maze: Maze3D, solverEntIndex=None):
        # Initialize maze with all walls
        maze.initCells(True)

        # Retrieve entrances and exits
        entrances = maze.getEntrances()
        exits = maze.getExits()

        if not entrances or not exits:
            raise ValueError("No entrances or exits defined in the maze.")

        # Check if solver entrance index is within bounds
        if solverEntIndex is not None and (solverEntIndex < 0 or solverEntIndex >= len(entrances)):
            raise ValueError(f"Specified index of entrance that solver starts is out of bounds: {solverEntIndex}")

        # Start from the specified entrance if provided, otherwise use the first entrance
        startCoord = entrances[solverEntIndex] if solverEntIndex is not None else entrances[0]

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
            shuffle(neighbours)  # Shuffle to add randomness
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
            shuffle(neighbours)  # Shuffle to add randomness
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
                    if cell not in maze.getEntrances() and cell not in maze.getExits():
                        if row == 0:
                            maze.addWall(cell, Coordinates3D(level, row - 1, col))
                        if row == maze.rowNum(level) - 1:
                            maze.addWall(cell, Coordinates3D(level, row + 1, col))
                        if col == 0:
                            maze.addWall(cell, Coordinates3D(level, row, col - 1))
                        if col == maze.colNum(level) - 1:
                            maze.addWall(cell, Coordinates3D(level, row, col + 1))

