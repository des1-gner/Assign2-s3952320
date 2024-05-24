# -------------------------------------------------
# DON'T CHANGE THIS FILE.
# Maze implementation for 3D mazes. 
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------

from typing import List, Tuple
from enum import Enum

from maze.util import Coordinates3D, WallCoordinates
from maze.graph import Graph
from maze.adjListGraph import AdjListGraph




class Maze3D:
    """
    Class representing for 3D mazes.  Different from Assignment 1, now we only have a single class representing
    a maze (and no need for you to implement one).
    """

    # Inner class, used to define constants, for indicating which indices corresond to what for list storing
    # level dimensions information.
    # (rowNum, colNum)
    class LevelDimsIndex(Enum):
        ROW_NUM = 0
        COL_NUM = 1



    def __init__(self, levelDims: List[Tuple[int, int]]):
        """
        Constructor.

        @param levelDims: list of tuples storing the specifications of each level in our maze, starting at level 0.
            Each tuple is (rowNum, colNum), where rowNum and colNum are the number of rows and columns for that level.
            The left, bottom cell for each level is always (0,0).
        """

        # (rowNum, colNum)
        # self.m_levelDims: stores the dimensions/specifications for each level in this 3D maze.  
        self.m_levelDims: List[Tuple[int, int]] = levelDims
        
        # list of entrances and exits.
        self.m_entrance: List[Coordinates3D] = list()
        self.m_exit: List[Coordinates3D] = list()

        # self.m_graph: We use an adjacency list representation to store our neighbourhoods and wall information.
        self.m_graph : Graph = AdjListGraph()



    def initCells(self, addWallFlag:bool = False):
        """
        Initialises the cells in the maze. 

        @param addWallFlag: Whether we should also add the walls between all adjacent cells as we are initiasing
            the maze.  Default is False.
        """
        
        # Loop through each level, and add the cells/vertices and neighbourhoods/edges to the graph representation.
        for level, (rowNum, colNum) in enumerate(self.m_levelDims):
            self.m_graph.addVertices([Coordinates3D(level,r,c) for r in range(0, rowNum) for c in range(0, colNum)])
            # add boundary vertices
            self.m_graph.addVertices([Coordinates3D(level,-1,c) for c in range(0, colNum)])
            self.m_graph.addVertices([Coordinates3D(level,r,-1) for r in range(0, rowNum)])
            self.m_graph.addVertices([Coordinates3D(level,rowNum,c) for c in range(0, colNum)])
            self.m_graph.addVertices([Coordinates3D(level,r,colNum) for r in range(0, rowNum)])

            # add adjacenies/edges to the graph
            # Scan across rows first and add edges between cells of each row
            for row in range(0, rowNum):
                for col in range(-1, colNum):
                    self.m_graph.addEdge(Coordinates3D(level,row,col), Coordinates3D(level,row,col+1), addWallFlag)

            # scan columns now and add edges between cells of each column
            for col in range(0, colNum):
                for row in range(-1, rowNum):
                    self.m_graph.addEdge(Coordinates3D(level,row,col), Coordinates3D(level,row+1,col), addWallFlag)

        # add edges between cells of different levels
        # should only do this after creation of vertices/cells
        levelNum = len(self.m_levelDims)
        for level in range(0,levelNum-1):
            # get current level stats
            (lowerRowNum, lowerColNum) = self.m_levelDims[level]
            (upperRowNum, upperColNum) = self.m_levelDims[level+1]
            # for each cell/vertex in lower level, check if there is a cell above it
            for row in range(0, lowerRowNum):
                for col in range(0, lowerColNum):
                    # no cell above it, means we need to add one and add an edge to mark it as a boundary
                    if not self.m_graph.hasVertex(Coordinates3D(level+1,row,col)):
                        self.m_graph.addVertex(Coordinates3D(level+1, row, col))
                    # then in both cases, whether there is an existing cell or just added a vertex for upper boundary,
                    # add the edge
                    self.m_graph.addEdge(Coordinates3D(level,row,col), Coordinates3D(level+1,row,col), addWallFlag)

            # for each cell/vertex in upper level, check if there is a cell below it
            for rowU in range(0, upperRowNum):
                for colU in range(0, upperColNum):
                    # no cell below it, means we need to add one and add an edge to mark it as a boundary
                    if not self.m_graph.hasVertex(Coordinates3D(level,rowU,colU)):
                        self.m_graph.addVertex(Coordinates3D(level, rowU, colU))
                    # then in both cases, whether there is an existing cell or just added a vertex for upper boundary,
                    # add the edge
                    self.m_graph.addEdge(Coordinates3D(level+1,rowU,colU), Coordinates3D(level,rowU,colU), addWallFlag)
                        
                        

    def addWall(self, cell1:Coordinates3D, cell2:Coordinates3D):
        """
        Adds a wall between cells cell1 and cell2.
        cell1 and cell2 should be adjacent.

        @param cell1: Coordinates of cell1.
        @param cell2: Coordinates of cell2.
        """
        # checks if Coordinates3D are valid
        assert(self.checkCoordinates(cell1) and self.checkCoordinates(cell2))
        
        self.m_graph.updateWall(cell1, cell2, True)



    def removeWall(self, cell1:Coordinates3D, cell2:Coordinates3D):
        """
        Removes a wall between cells cell1 and cell2.
        cell1 and cell2 should be adjacent.

        @param cell1: Coordinates of cell1.
        @param cell2: Coordinates of cell2.

        """
        # checks if Coordinates3D are valid
        assert(self.checkCoordinates(cell1) and self.checkCoordinates(cell2))

        self.m_graph.updateWall(cell1, cell2, False)



    def neighbours(self, cell:Coordinates3D)->List[Coordinates3D]:
        """
        @param cell: Cell we want to find the neighbours for.

        @returns: Return the neighbours of cell.
        """
        return self.m_graph.neighbours(cell)



    def neighbourWalls(self, cell:Coordinates3D)->List[WallCoordinates]:
        """
        @param cell: Cell we want to find the adjacent walls for.

        @returns: Return the coordinates of walls that are neighbours of cell.
        """
        return self.m_graph.neighbourWalls(cell)



    def allCells(self)->List[Coordinates3D]:
        """
        @returns: Return all cells in the maze.
        """
        return self.m_graph.vertices()



    def storeEntrance(self, cell: Coordinates3D)->bool:
        """
        Adds an entrance to the maze.  A maze can have more than one entrance, so this method can be called more than once.
        This does not remove the wall between entrance and maze.

        @returns: True if successfully added an entrance, otherwise False.
        """

        # check if cell of entrance is valid
        assert(self.checkCoordinates(cell))

        # check if cell of the entrance is on the boundary of the maze, as an entrance should only be added along the boundary
        if self.isBoundary(cell):
            self.m_entrance.append(cell)

            return True
        else:
            # not on the boundary
            return False



    def storeExit(self, cell: Coordinates3D)->bool:
        """
        Adds an exit to the maze.  A maze can have more than one exit, so this method can be called more than once.
        This does not remove the wall between maze and exit.

        @returns True if successfully added an exit, otherwise False.
        """

        # check if cell of exit is valid
        assert(self.checkCoordinates(cell))

        # check if cell of exit is on the boundary of the maze, as an exit should only be added along the boundary
        if self.isBoundary(cell):
            self.m_exit.append(cell)

            return True
        else:
            # not on boundary
            return False
        


    def carveEntrances(self):
        """
		Carve the stored entrance(s) of the maze.  This involves removing the necessary walls between the entrances
        and the maze.
		"""

		# when adding the entrances, we need to remove the relevant boundary wall
        for ent in self.m_entrance:
            currLevel = ent.getLevel()
			# get level specs
            (rowNum, colNum) = self.m_levelDims[currLevel]

			# need to figure out which direction to remove wall
			# entrance is at bottom, need to remove wall in "up" direction
            if ent.getRow() == -1:
                self.removeWall(ent, Coordinates3D(currLevel, 0, ent.getCol()))
			# entrance is at top, need to remove wall in "down" direction
            elif ent.getRow() == rowNum:
                self.removeWall(ent, Coordinates3D(currLevel, rowNum-1, ent.getCol()))
			# entrace is to the left, need to remove wall in "right" direction
            elif ent.getCol() == -1:
                self.removeWall(ent, Coordinates3D(currLevel, ent.getRow(), 0))
			# entrance is to the right, need to remove wall in "left" direction
            elif ent.getCol() == colNum:
                self.removeWall(ent, Coordinates3D(currLevel, ent.getRow(), colNum-1))



    def carveExits(self):
        """
		Carve exit(s) of the maze.  This involves removing the necessary walls between the exits
        and the maze.
		"""

		# when adding the exits, we need to remove the relevant boundary wall and add neighbouring edges
        for ext in self.m_exit:
            currLevel = ext.getLevel()
			# get level specs
            (rowNum, colNum) = self.m_levelDims[currLevel]

			# need to figure out which direction to remove wall
			# exit is at bottom, need to remove wall in "up" direction
            if ext.getRow() == -1:
                self.removeWall(ext, Coordinates3D(currLevel, 0, ext.getCol()))
			# exit is at top, need to remove wall in "down" direction
            elif ext.getRow() == rowNum:
                self.removeWall(ext, Coordinates3D(currLevel, rowNum-1, ext.getCol()))
			# exit is to the left, need to remove wall in "right" direction
            elif ext.getCol() == -1:
                self.removeWall(ext, Coordinates3D(currLevel, ext.getRow(), 0))
			# exit is to the right, need to remove wall in "left" direction
            elif ext.getCol() == colNum:
                self.removeWall(ext, Coordinates3D(currLevel, ext.getRow(), colNum-1))
        


    def getEntrances(self)->List[Coordinates3D]:
        """
        @returns: List of entrances that the maze has.
        """
        return self.m_entrance
    


    def getExits(self)->List[Coordinates3D]:
        """
        @returns: List of exits that the maze has.
        """
        return self.m_exit



    def hasCell(self, cell:Coordinates3D)->bool:
        """
        Checks if cell exists in maze.

        @param: Cell we are checking.

        @returns True, if the cell exists.

        """
        return self.m_graph.hasVertex(cell)



    def hasWall(self, cell1:Coordinates3D, cell2:Coordinates3D)->bool:
        """
        Checks if there is a wall between cell1 and cell2.

        @param cell1: One side of wall.
        @param cell2: Other side of wall.

        @returns True, if there is a wall between the two specified cells.

        """
        return self.m_graph.getWallStatus(cell1, cell2)



    def rowNum(self, level: int)->int:
        """
        @param: Level we want to retrieve the number of rows for.

        @returns The number of rows the maze has at level.
        """
        assert(level >= 0 and level < len(self.m_levelDims))
        return self.m_levelDims[level][self.LevelDimsIndex.ROW_NUM.value]



    def colNum(self, level: int)->int:
        """
        @param: Level we want to retrieve the number of columns for.

        @returns The number of columns the maze has.
        """
        assert(level >= 0 and level < len(self.m_levelDims))
        return self.m_levelDims[level][self.LevelDimsIndex.COL_NUM.value]
    


    def levelNum(self)->int:
        """
        @returns The number of levels the maze has.
        """
        return len(self.m_levelDims)
    


    def cellNum(self, level: int)->int:
        """
        @param level: The level in which we want to find the number of cells has.

        @returns The number of cells the maze has.
        """

        assert(level >= 0 and level < len(self.m_levelDims))
        return self.rowNum(level) * self.colNum(level)



    def checkCoordinates(self, coord:Coordinates3D)->bool:
        """
        Checks if the coordinates is a valid one.
        
        @param coord: Cell/coordinate to check if it is a valid one.
        
        @returns True if coord/cell is valid, otherwise False.
        """

        level: int = coord.getLevel()
        row: int = coord.getRow()
        col: int = coord.getCol()

        # check level is valid
        assert(level >= 0 and level < len(self.m_levelDims))

        # get the appropriate specs for that level
        (rowNum, colNum) = self.m_levelDims[level]

        return row >= -1 and row <= rowNum and col >= -1 and col <= colNum
    


    def isBoundary(self, coord:Coordinates3D)->bool:
        """
        Checks if the coordinates is on the boundary
        
        @param coord: Cell/coordinate to check if it is on the boundary.
        
        @returns True if coord/cell is on the boundary, otherwise False.
        """        
        level: int = coord.getLevel()
        row: int = coord.getRow()
        col: int = coord.getCol()

        # check level is valid
        assert(level >= 0 and level < len(self.m_levelDims))

        # get the appropriate specs for that level
        (rowNum, colNum) = self.m_levelDims[level]
        
        return row == -1 or row == rowNum or col == -1 or col == colNum



    