# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# This is the entry point to run the program.
# Refer to usage() for exact format of input expected to the program.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


import sys
import time
import json
import random
from typing import List, Tuple

from generatorSelector import GeneratorSelector
from solverSelector import SolverSelector

from solving.mazeSolver import MazeSolver
from generation.mazeGenerator import MazeGenerator

from maze.util import Coordinates3D
from maze.maze3D import Maze3D



# this checks if Visualizer has been imported properly.
# if not, likely missing some packages, e.g., matplotlib.
# in that case, regardless of visualisation flag, we should set the canVisualise flag to False which will not call the visuslisation part.
canVisualise = True
try:
	from maze.maze_viz import Visualizer
except:
	Visualizer = None
	canVisualise = False



def usage():
	"""
	Print help/usage message.
	"""

	# On Teaching servers, use 'python3'
	# On Windows, you may need to use 'python' instead of 'python3' to get this to work
	print('python3 mazeTester2.py', '<configuration file>')
	sys.exit(1)


#
# Main function, when the python script is executed, we execute this.
#
if __name__ == '__main__':
	# Fetch the command line arguments
	args = sys.argv

	if len(args) != 2:
		print('Incorrect number of arguments.')
		usage()


	# open configuration file		
	fileName: str = args[1]
	with open(fileName,"r") as configFile:
		# use json parser
		configDict = json.load(configFile)

		#
		# Assign to variables storing various parameters.
		#
	
		# specifications of each level
		levelSpecs: List[List[int]] = configDict['levelSpecs']
		# set of entrances
		entrances: List[List[int]] = configDict['entrances']
		# set of exits
		exits: List[List[int]] = configDict['exits']
		# generator approach to use (appropriate for Tasks A, B, C)
		genApproach: str = configDict['generator']
		# solver approach to use (appropriate for Tasks A, B and D)
		solverApproach: str = configDict['solver']
		# Optional: The index of which entrance to use (start at index 0) (appropraite for Tasks A, B and D)
		solverEntIndex = None
		if 'solverEntranceIndex' in configDict.keys():
			solverEntIndex: int = configDict['solverEntranceIndex']
		# whether to visualise the generated maze and solving solution or not
		bVisualise: bool = configDict['visualise']
		# Optional: Filename to store visualisation output
		outFilename : str = None
		if 'fileOutput' in configDict.keys():
			outFilename = configDict['fileOutput']
		# Optional: Seed to pass to random generator (used for validation)
		randSeed: int = None
		if 'randSeed' in configDict.keys():
			randSeed = configDict['randSeed']


		# initialise the random seed generator 
		if randSeed != None:
			random.seed(randSeed)


		#
		# Initialise maze object.
		#
		maze: Maze3D = Maze3D(levelSpecs)

		# Store the entrances and exits.
		for [l,r,c] in entrances:
			maze.storeEntrance(Coordinates3D(l, r, c))
		for [l,r,c] in exits:
			maze.storeExit(Coordinates3D(l, r, c))

		
		#
		# Construct maze solver.  The solverSelector allows us to abstract away the selection and update its 
		# implementation as needed, without affecting the code in this file.
		# You can implement extra solvers, just make sure to update the list of solvers here
		#
		solverSelector: SolverSelector = SolverSelector()
		solver: MazeSolver = solverSelector.construct(solverApproach)
		
		# if solver is None, means it is an unknown solver
		if solver == None:
			print('{} is an unknown solver approach.'.format(solverApproach))
			usage()  


		# 
		# Construct maze generator.  There are two ways to call generator.match, depending if it is for taskD or
		# other tasks.
		#
		generator: MazeGenerator = None
		genSelector: GeneratorSelector = GeneratorSelector()

		if genApproach == 'taskD':
			# this will select the generator based on the solver.
			generator = genSelector.match(solver)
		else: 
			# this will select the generator according to specified input.
			generator = genSelector.construct(genApproach)

			# if generator is None, means it is an unknown generator
			if generator == None:
				print('{} is an unknown generator approach.'.format(genApproach))
				usage()



		#
		# Generate maze.
		#

		# timer for generation
		startGenTime : float = time.perf_counter()

		generator.generateMaze(maze)

		# stop timer
		endGenTime: float = time.perf_counter()

		print(f'Generation took {endGenTime - startGenTime:0.4f} seconds')

		# carve out the entrances and exits
		maze.carveEntrances()
		maze.carveExits()



		#
		# Solve maze
		#
		mazeEntrances: List[Coordinates3D]  = maze.getEntrances()

		# check if solver entrance index is within bounds (this is used for Tasks A, B and D)
		if solverEntIndex != None and (solverEntIndex < 0 or solverEntIndex >= len(mazeEntrances)):
			print("Specified index of entrance that solver starts is out of bounds, {}".format(solverEntIndex))
			usage()

		if generator.isMazeGenerated():
			# time for solving
			startSolveTime : float = time.perf_counter()

			# Task A, B and D mode, where we specify the entrance
			if solverEntIndex != None:
				solver.solveMaze(maze, mazeEntrances[solverEntIndex])
			else:
				# Task C, where it is part of the task to find the "best" entrances and exits
				solver.solveMaze(maze)
			
			# stop timer
			endSolveTime: float = time.perf_counter()

			print(f'Solving took {endSolveTime - startSolveTime:0.4f} seconds')
			print(f'Solver explored {solver.getCellsExplored()} number of cells.')
			print('Solver used Entrance {entrance} and Exit {exit}.'.format(entrance=solver.getEntranceUsed(), exit=solver.getExitUsed()))
		else:
			print("Generator hasn't been implemented yet, hence solver wasn't called.")


		#
		# Display maze.
		#
		if bVisualise and canVisualise and generator.isMazeGenerated():
			cellSize = 1
			visualiser = Visualizer(maze, solver, cellSize) 
			if outFilename == None:
				visualiser.show_maze()
			else:
				visualiser.show_maze(outFilename)




			
