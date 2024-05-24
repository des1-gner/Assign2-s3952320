# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Recursive backtracking maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import randint, choice
from collections import deque

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator




class RecurBackMazeGenerator(MazeGenerator):
	"""
	Recursive backtracking maze generator.  This is one of the provided generators.  Study this for ideas on 
	how to implement the other generators of Task A.
	"""

	def generateMaze(self, maze: Maze3D):
		# make sure we start the maze with all walls there
		maze.initCells(True)

		# select starting cell 
		# random floor
		startLevel = randint(0, maze.levelNum()-1)
		startCoord : Coordinates3D = Coordinates3D(startLevel, randint(0, maze.rowNum(startLevel)-1), randint(0, maze.colNum(startLevel)-1))

		# run recursive backtracking/DFS from starting cell
		stack : deque = deque()
		stack.append(startCoord)
		currCell : Coordinates3D = startCoord 
		visited : set[Coordinates3D] = set([startCoord])

		totalCells = sum([maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum())])

		while len(visited) < totalCells:
			# find all neighbours of current cell
			neighbours : list[Coordinates3D] = maze.neighbours(currCell)

			# filter to ones that haven't been visited and within boundary
			nonVisitedNeighs : list[Coordinates3D] = [neigh for neigh in neighbours if neigh not in visited and\
											 neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and\
												neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel())]
			
			# see if any unvisited neighbours
			if len(nonVisitedNeighs) > 0:
				# randomly select one of them
				neigh = choice(nonVisitedNeighs)

				# we move there and knock down wall
				maze.removeWall(currCell, neigh)

				# add to stack
				stack.append(neigh)

				# updated visited
				visited.add(neigh)

				# update currCell
				currCell = neigh
			else:
				# backtrack
				currCell = stack.pop()

		# update maze generated
		self.m_mazeGenerated = True

		
