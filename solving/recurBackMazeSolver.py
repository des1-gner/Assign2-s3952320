# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Recursive backtracking maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import choice
from collections import deque

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D


class RecurBackMazeSolver(MazeSolver):
    """
    Recursive backtracking solver implementation.  Provided implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "recur"



    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False

		# select starting cell
        startCoord: Coordinates3D = entrance

		# run recursive backtracking/DFS from starting cell
        stack : deque = deque()
        # stack.append(startCoord)
        currCell : Coordinates3D = startCoord 
        visited : set[Coordinates3D] = set([startCoord])

        self.solverPathAppend(startCoord, False)

    
        while currCell not in maze.getExits():
			# find all neighbours of current cell
            neighbours : list[Coordinates3D] = maze.neighbours(currCell)

			# filter to ones that haven't been visited and within boundary and doesn't have a wall between them	
            nonVisitedNeighs : list[Coordinates3D] = [neigh for neigh in neighbours if neigh not in visited and not maze.hasWall(currCell,neigh) and\
											 (neigh.getRow() >= -1) and (neigh.getRow() <= maze.rowNum(neigh.getLevel())) and\
												(neigh.getCol() >= -1) and (neigh.getCol() <= maze.colNum(neigh.getLevel()))]

			# see if any unvisited neighbours
            if len(nonVisitedNeighs) > 0:
				# randomly select one of them
                neigh = choice(nonVisitedNeighs)

				# add to stack
                stack.append(neigh)

				# updated visited
                visited.add(neigh)
                self.solverPathAppend(neigh, False)

				# update currCell
                currCell = neigh
            else:
				# backtrack
                currCell = stack.pop()
                currCell = stack.pop()
                stack.append(currCell)
                self.solverPathAppend(currCell, True)

        # ensure we are currently at the exit
        if currCell in maze.getExits():
            self.solved(entrance, currCell)

	

