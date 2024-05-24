# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Abstract class for a maze solver.  Provides common variables and method interface for maze solvers.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from typing import List, Tuple
from maze.maze3D import Maze3D
from maze.util import Coordinates3D


class MazeSolver:

    def __init__(self):
        # self.m_solved: true if the solver has found the exit (maze "solved")
        self.m_solved = False
        # self.m_cellsExplored: Number of cells explored during the solving process.  Does not include backtracking.
        self.m_cellsExplored = 0    
        # self.m_solverPath: Set of cells that the solver visited.  This does include backtracking.
        self.m_solverPath: List[Tuple[Coordinates3D, bool]] = list()
        # self.m_entranceUsed: Entrance used to enter maze by the solver.
        self.m_entranceUsed = None
        # self.m_exitUsed: Exit found and used by maze solver as the exit.
        self.m_exitUsed = None
        # name of the solver
        self.m_name = ""



    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        """
        Abstract method to solve the maze.  This is used by Tasks A, B and D, where the entrance is provided.

        @param maze: Instance of maze to solve.
        @param entrance: Entrance that the solver enters the maze.
        """
        pass



    def solveMazeTaskC(self, maze: Maze3D):
        """
        Abstract method to solve the maze.  This is used by Task C.
        This version of solveMaze does not provide a starting entrance, and as part of the solution, the method should
        to find the entrance and exit pair (see project specs for requirements of this task).

        @param maze: Instance of maze to solve.
        """
        pass



    def solved(self, entrance: Coordinates3D, exit: Coordinates3D):
        """
        If solver has solved the maze, call this method with the entrance and exit to update the solver about this.

        @param entrance: Entrance used in the solution.
        @param exit: Exit used in the solution.
        """
        self.m_solved = True
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit



    def isSolved(self)->bool:
        """
        Use after solveMaze(maze), to check whether the maze is solved/solver has found a solution.

	    @return True if solved. Otherwise false.
        """
        return self.m_solved


    def solverPathAppend(self, cell: Coordinates3D, isBacktrack: bool = False):
        """
        Use to append a cell visited by solver.  Will also increment the number of cells explored.  Make sure this is
        called everything a cell is explored, as it will be used in both the visualisation and for counting the number
        of cells visited.

        @param cell: Cell to add to the path.
        @param isBacktrack: Whether the cell is visited because of backtrakcing (set to True) or first visited (set to False).  Default is False.
        """
        # we don't update cells explored for backtracking
        if not isBacktrack:
            self.m_cellsExplored += 1
        self.m_solverPath.append((cell, isBacktrack))



    def resetPathAndCellExplored(self):
        """
        Reset the number of cells explored and solver path.
        """
        self.m_cellsExplored = 0
        self.m_solverPath = list()



    def getCellsExplored(self)->int:
        """
        Use after solveMaze(maze), counting the number of cells explored in solving process.

	    @return The number of cells explored.
        """
        return self.m_cellsExplored
	


    def getSolverPath(self)->List[Tuple[Coordinates3D, bool]]:
        """
        @return The path that the solver went through, which includes both cells visited and cells traversed when backtracking.
        """
        return self.m_solverPath
    
    

    def getEntranceUsed(self)->Coordinates3D:
        """
        @return Return the entrance used in the solution.  Should only be called after a solution is found.
        """
        return self.m_entranceUsed



    def getExitUsed(self)->Coordinates3D:
        """
        @return Return the exit used in the solution.  Should only be called after a solution is found.
        """
        return self.m_exitUsed
    

