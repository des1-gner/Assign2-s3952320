# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Task C solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D



class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation.  You'll need to complete its implementation for task C.
    """


    def __init__(self):
        super().__init__()
        self.m_name = "taskC"



    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        # we call the the solve maze call without the entrance.
        # DO NOT CHANGE THIS METHOD
        self.solveMazeTaskC(maze)



    def solveMazeTaskC(self, maze: Maze3D):
        """       
        solve the maze, used by Task C.
        This version of solveMaze does not provide a starting entrance, and as part of the solution, the method should
        to find the entrance and exit pair (see project specs for requirements of this task).
        TODO: Please complete this implementation for task C.  You should call maze.solved(...) to update which entrance
        and exit you used for task C.

        @param maze: Instance of maze to solve.

        """
        pass






    

