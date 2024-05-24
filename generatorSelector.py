# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Abstract class for a maze solver.  Provides common variables and method interface for maze solvers.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from generation.mazeGenerator import MazeGenerator
from generation.recurBackGenerator import RecurBackMazeGenerator
from generation.primGenerator import PrimMazeGenerator
from generation.wilsonGenerator import WilsonMazeGenerator
from generation.taskDMazeGenerator import TaskDMazeGenerator
from solving.mazeSolver import MazeSolver


class GeneratorSelector:
    """
    Class used to select and construct appropriate maze generator.
    """


    def construct(self, genApproach: str)->MazeGenerator:
        """
        Tasks A, B and C, with a specified maze generator.
        If genApproach is unknown, None will be returned.

        @param genApproach: Name of generator to use.
        
        @return: Instance of a maze generator.
        """
        generator: MazeGenerator = None

        if genApproach == 'recur':
            generator = RecurBackMazeGenerator()
        elif genApproach == 'prim':
            generator = PrimMazeGenerator()
        elif genApproach == 'wilson':
            generator = WilsonMazeGenerator()
        # TODO: If you implement other generators, you can add them here

        return generator



    def match(self, solver: MazeSolver)->MazeGenerator:
        """
        Task D, with a specified maze generator.
        A solver is provided, and you can access the particularly solver by calling its name() method.
        TODO: You are to complete the implementation of this if attempting Task D.

        @param solver: Instance of a maze solver you should generate a maze to maximum the number of cells it explroes.
        
        @return: Instance of a maze generator.
        """

        generator: MazeGenerator = None

        # TODO: Complete implementation for Task D, which also involves selection of appropriate generator.
        # The passed solver can be used to query the name of it, but you are not allowed to run the solver before
        # generating the maze.

        # TODO: Default option is to use Task D generator.  Note you do not have to use this, but this is provided in case
        # you wanted to build a custom generator, rather than select an existing one.
        # Remove / comment this out once if you not using this.
        generator = TaskDMazeGenerator()

        return generator
