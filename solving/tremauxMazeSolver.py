# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Tremaux's Algorithm maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import choice
from collections import deque

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D


class TremauxMazeSolver(MazeSolver):
    """
    Tremaux's Algorithm solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "tremaux"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False

        # select starting cell
        startCoord: Coordinates3D = entrance

        # stack to keep track of the path
        stack: deque = deque()
        stack.append(startCoord)

        # dictionary to keep track of the number of visits to each cell
        visit_count: dict[Coordinates3D, int] = {startCoord: 1}

        currCell: Coordinates3D = startCoord
        self.solverPathAppend(startCoord, False)

        while currCell not in maze.getExits():
            neighbours: list[Coordinates3D] = maze.neighbours(currCell)

            nonVisitedNeighs: list[Coordinates3D] = [neigh for neigh in neighbours if neigh not in visit_count and not maze.hasWall(currCell, neigh)]
            visitedOnceNeighs: list[Coordinates3D] = [neigh for neigh in neighbours if visit_count.get(neigh, 0) == 1 and not maze.hasWall(currCell, neigh)]
            
            if nonVisitedNeighs:
                neigh = choice(nonVisitedNeighs)
                stack.append(neigh)
                visit_count[neigh] = 1
                self.solverPathAppend(neigh, False)
                currCell = neigh
            elif visitedOnceNeighs:
                neigh = choice(visitedOnceNeighs)
                stack.append(neigh)
                visit_count[neigh] = 2
                self.solverPathAppend(neigh, False)
                currCell = neigh
            else:
                currCell = stack.pop()
                self.solverPathAppend(currCell, True)

        if currCell in maze.getExits():
            self.solved(entrance, currCell)


