# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Base class for maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from maze.util import Coordinates3D

class MazeGenerator:
	"""
	Base class for a maze generator.
	"""

	
	def __init__(self):
		# This is used to indicate to program whether a maze been generated, or nothing has been done.
		# Need to set this to true once a maze is generated!
		self.m_mazeGenerated: bool = False



	def generateMaze(self, maze:Maze3D):
		"""
	    Generates a maze.  Will update the passed maze.

		@param maze: Maze which we update on to generate a maze. 
		"""
		pass



	def isMazeGenerated(self)->bool:
		"""
		@return: Whether a maze has been generated, or False if just an empty method call.
		"""
		return self.m_mazeGenerated

		