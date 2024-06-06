from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from collections import deque
import random

class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation using a biased random walk algorithm.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        """
        solve the maze, used by Task C.
        """
        self.m_solved = False

        startCoord: Coordinates3D = entrance
        stack: deque = deque()
        currCell: Coordinates3D = startCoord
        visited: set[Coordinates3D] = set([startCoord])

        self.solverPathAppend(startCoord, False)

        while currCell not in maze.getExits():
            neighbours: list[Coordinates3D] = maze.neighbours(currCell)
            nonVisitedNeighs: list[Coordinates3D] = [neigh for neigh in neighbours if neigh not in visited and not maze.hasWall(currCell, neigh) and
                                                     (neigh.getRow() >= -1) and (neigh.getRow() <= maze.rowNum(neigh.getLevel())) and
                                                     (neigh.getCol() >= -1) and (neigh.getCol() <= maze.colNum(neigh.getLevel()))]

            if len(nonVisitedNeighs) > 0:
                # Bias towards the direction of the nearest exit
                nonVisitedNeighs.sort(key=lambda cell: min(abs(cell.getRow() - exit.getRow()) + abs(cell.getCol() - exit.getCol()) + abs(cell.getLevel() - exit.getLevel())
                                                            for exit in maze.getExits()))
                nextCell = nonVisitedNeighs[0]

                stack.append(nextCell)
                visited.add(nextCell)
                self.solverPathAppend(nextCell, False)
                currCell = nextCell
            else:
                if stack:
                    currCell = stack.pop()
                    self.solverPathAppend(currCell, True)
                else:
                    break

        if currCell in maze.getExits():
            self.solved(entrance, currCell)


