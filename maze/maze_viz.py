# -------------------------------------------------
# DON'T CHANGE THIS FILE.
# Visualiser, original code from https://github.com/jostbr/pymaze writteb by Jostein Brændshøi
# Subsequentially modified by Jeffrey Chan.
#
# __author__ = 'Jostein Brændshøi, Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------

# MIT License

# Copyright (c) 2021 Jostein Brændshøi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



try:
    import matplotlib.pyplot as plt
except:
    plt = None
    

from math import ceil

from maze.maze3D import Maze3D
from maze.util import Coordinates3D

from solving.mazeSolver import MazeSolver


class Visualizer(object):
    """Class that handles all aspects of visualization.


    Attributes:
        maze: The maze that will be visualized
        cell_size (int): How large the cells will be in the plots
        height (int): The height of the maze
        width (int): The width of the maze
        ax: The axes for the plot
    """

    def __init__(self, maze: Maze3D, solver: MazeSolver, cellSize):
        self.m_maze = maze
        self.m_solver = solver
        self.m_cellSize = cellSize
        self.m_ax = None
        # pixel adjustments for each level, used for aligning the visualisation of each level.
        self.m_levelAdjust: list[tuple[int, int]] = list()



    def show_maze(self, outFilename: str = None):
        """
        Displays a plot of the maze with the solution path.
        """

        # provide an error message if matplotlib isn't installed.
        if plt == None:
            print("Matplotlib not available on this computer.  Visualisation is not possible.")
            exit(1)

        # create the plot figure and style the axes
        fig = self.configure_plot()

        # plot the walls on the figure
        self.plot_walls()

        # plot the entrances and exits on the figure
        self.plotEntExit()

        # plot the solver path
        if self.m_solver != None:
            self.plotSolverPath()

        # display the plot to the user
        if outFilename == None:
            plt.show()
        else:
            # save image
            plt.savefig(outFilename)



    def plot_walls(self):
        """ 
        Plots the walls of a maze. This is used when generating the maze image.
        """
        
        # plot levels
        # plot them in two rows
        firstColMazeNum = ceil(self.m_maze.levelNum() / 2)
        # first column/left column 
        shiftPixelX: int = 0
        shiftPixelY: int = 0
        for level in range(0, firstColMazeNum):
            # plot each level/floor of maze
            for r in range(0, self.m_maze.rowNum(level)):
                for c in range(0, self.m_maze.colNum(level)):
                    # top
                    if self.m_maze.hasWall(Coordinates3D(level, r-1, c), Coordinates3D(level, r, c)):
                        self.m_ax.plot([(c+1)*self.m_cellSize, (c+1+1)*self.m_cellSize],
                                    [(r+1)*self.m_cellSize + shiftPixelY, (r+1)*self.m_cellSize + shiftPixelY], color="k")    
                    # left
                    if self.m_maze.hasWall(Coordinates3D(level, r, c-1), Coordinates3D(level, r, c)):
                        self.m_ax.plot([(c+1)*self.m_cellSize, (c+1)*self.m_cellSize],
                                    [(r+1)*self.m_cellSize + shiftPixelY, (r+1+1)*self.m_cellSize + shiftPixelY], color="k")  
            
                    # do up and down passages
                    if level-1 >= 0:
                        if not self.m_maze.hasWall(Coordinates3D(level, r, c), Coordinates3D(level-1, r, c)):
                            self.m_ax.plot([(c+1.5)*self.m_cellSize], [(r+1.5)*self.m_cellSize + shiftPixelY], 'vb')
                            

                    if level+1 < self.m_maze.levelNum():
                        if not self.m_maze.hasWall(Coordinates3D(level, r, c), Coordinates3D(level+1, r, c)):
                            self.m_ax.plot([(c+1.5)*self.m_cellSize], [(r+1.5)*self.m_cellSize + shiftPixelY], '^r')
                            


            # do bottom boundary 
            for c in range(0, self.m_maze.colNum(level)):
                # top
                if self.m_maze.hasWall(Coordinates3D(level, self.m_maze.rowNum(level)-1, c), Coordinates3D(level, self.m_maze.rowNum(level), c)):
                    self.m_ax.plot([(c+1)*self.m_cellSize, (c+1+1)*self.m_cellSize],
                                    [(self.m_maze.rowNum(level)+1)*self.m_cellSize + shiftPixelY, (self.m_maze.rowNum(level)+1)*self.m_cellSize + shiftPixelY], color="k")    

            # do right boundary 
            for r in range(0, self.m_maze.rowNum(level)):
                # left
                if self.m_maze.hasWall(Coordinates3D(level, r, self.m_maze.colNum(level)-1), Coordinates3D(level, r, self.m_maze.colNum(level))):
                    self.m_ax.plot([(self.m_maze.colNum(level)+1)*self.m_cellSize, (self.m_maze.colNum(level)+1)*self.m_cellSize],
                                    [(r+1)*self.m_cellSize + shiftPixelY, (r+1+1)*self.m_cellSize + shiftPixelY], color="k")  


            # print out level label
            self.m_ax.text(-0.5, shiftPixelY, "Level " + str(level), fontsize=10, weight="bold")

            self.m_levelAdjust.append((0, shiftPixelY))

            shiftPixelY += (self.m_maze.rowNum(level)+5) * self.m_cellSize
            shiftPixelX = max(shiftPixelX, (self.m_maze.rowNum(level)+5) * self.m_cellSize)


        # second column/right column
        shiftPixelY = 0
        for level in range(firstColMazeNum, self.m_maze.levelNum()):
            # plot each level/floor of maze
            for r in range(0, self.m_maze.rowNum(level)):
                for c in range(0, self.m_maze.colNum(level)):
                    # top
                    if self.m_maze.hasWall(Coordinates3D(level, r-1, c), Coordinates3D(level, r, c)):
                        self.m_ax.plot([(c+1)*self.m_cellSize + shiftPixelX, (c+1+1)*self.m_cellSize + shiftPixelX],
                                    [(r+1)*self.m_cellSize + shiftPixelY, (r+1)*self.m_cellSize + shiftPixelY], color="k")    
                    # left
                    if self.m_maze.hasWall(Coordinates3D(level, r,c-1), Coordinates3D(level, r,c)):
                        self.m_ax.plot([(c+1)*self.m_cellSize + shiftPixelX, (c+1)*self.m_cellSize + shiftPixelX],
                                    [(r+1)*self.m_cellSize + shiftPixelY, (r+1+1)*self.m_cellSize + shiftPixelY], color="k")  
                        
                    # do up and down passages
                    if level-1 >= 0:
                        if not self.m_maze.hasWall(Coordinates3D(level, r, c), Coordinates3D(level-1, r, c)):
                            self.m_ax.plot([(c+1.5)*self.m_cellSize + shiftPixelX], [(r+1.5)*self.m_cellSize + shiftPixelY], 'vb')
                                    

                    if level+1 < self.m_maze.levelNum():
                        if not self.m_maze.hasWall(Coordinates3D(level, r, c), Coordinates3D(level+1, r, c)):
                            self.m_ax.plot([(c+1.5)*self.m_cellSize + shiftPixelX], [(r+1.5)*self.m_cellSize + shiftPixelY], '^r')   
                 
                        
            # do bottom boundary 
            for c in range(0, self.m_maze.colNum(level)):
                # top
                if self.m_maze.hasWall(Coordinates3D(level, self.m_maze.rowNum(level)-1, c), Coordinates3D(level, self.m_maze.rowNum(level), c)):
                    self.m_ax.plot([(c+1)*self.m_cellSize + shiftPixelX, (c+1+1)*self.m_cellSize + shiftPixelX],
                                    [(self.m_maze.rowNum(level)+1)*self.m_cellSize + shiftPixelY, (self.m_maze.rowNum(level)+1)*self.m_cellSize + shiftPixelY], color="k")    

            # do right boundary 
            for r in range(0, self.m_maze.rowNum(level)):
                # left
                if self.m_maze.hasWall(Coordinates3D(level, r, self.m_maze.colNum(level)-1), Coordinates3D(level, r, self.m_maze.colNum(level))):
                    self.m_ax.plot([(self.m_maze.colNum(level)+1)*self.m_cellSize + shiftPixelX, (self.m_maze.colNum(level)+1)*self.m_cellSize + shiftPixelX],
                                    [(r+1)*self.m_cellSize + shiftPixelY, (r+1+1)*self.m_cellSize + shiftPixelY], color="k")  
            
     
            # print out level label
            self.m_ax.text(-0.5+shiftPixelX, shiftPixelY, "Level " + str(level), fontsize=10, weight="bold")
            

            self.m_levelAdjust.append((shiftPixelX, shiftPixelY))

            shiftPixelY += (self.m_maze.rowNum(level)+5) * self.m_cellSize



    def plotEntExit(self):
        """
        Plots the entrances and exits in the displayed maze.
        """

        # entrances
        for ent in self.m_maze.getEntrances():
            (shiftX, shiftY) = self.m_levelAdjust[ent.getLevel()]
            # check direction of arrow
            # upwards arrow
            if ent.getRow() == -1:
                self.m_ax.arrow((ent.getCol()+1.5)*self.m_cellSize + shiftX, (ent.getRow()+1)*self.m_cellSize + shiftY, 0, self.m_cellSize*0.6, head_width=0.1)
            # downwards arrow
            elif ent.getRow() == self.m_maze.rowNum(ent.getLevel()):
                self.m_ax.arrow((ent.getCol()+1.5)*self.m_cellSize + shiftX, (ent.getRow()+2)*self.m_cellSize + shiftY, 0, -self.m_cellSize*0.6, head_width=0.1)
            # rightward arrow
            elif ent.getCol() == -1:
                self.m_ax.arrow((ent.getCol()+1)*self.m_cellSize + shiftX, (ent.getRow()+1.5)*self.m_cellSize + shiftY, self.m_cellSize*0.6, 0, head_width=0.1)
            # leftward arrow
            elif ent.getCol() == self.m_maze.colNum(ent.getLevel()):
                self.m_ax.arrow((ent.getCol()+2)*self.m_cellSize + shiftX, (ent.getRow()+1.5)*self.m_cellSize + shiftY, -self.m_cellSize*0.6, 0, head_width=0.1)

        # exits
        for ext in self.m_maze.getExits():
            (shiftX, shiftY) = self.m_levelAdjust[ext.getLevel()]
            # downwards arrow
            if ext.getRow() == -1:
                self.m_ax.arrow((ext.getCol()+1.5)*self.m_cellSize + shiftX, (ext.getRow()+1.8)*self.m_cellSize + shiftY, 0, -self.m_cellSize*0.6, head_width=0.1)
            # upwards arrow
            elif ext.getRow() == self.m_maze.rowNum(ext.getLevel()):
                self.m_ax.arrow((ext.getCol()+1.5)*self.m_cellSize + shiftX, (ext.getRow()+1.2)*self.m_cellSize + shiftY, 0, self.m_cellSize*0.6, head_width=0.1)
            # leftward arrow
            elif ext.getCol() == -1:
                self.m_ax.arrow((ext.getCol())*self.m_cellSize + shiftX, (ext.getRow()+1.5)*self.m_cellSize + shiftY, -self.m_cellSize*0.6, 0, head_width=0.1)
            # leftward arrow
            elif ext.getCol() == self.m_maze.colNum(ext.getLevel()):
                self.m_ax.arrow((ext.getCol()+1.2)*self.m_cellSize + shiftX, (ext.getRow()+1.5)*self.m_cellSize + shiftY, self.m_cellSize*0.6, 0, head_width=0.1)



    def plotSolverPath(self):
        """
        Draw the path that the solver used to solve the maze.  They are displayed as a series of circles.
        """

        # retrieved the stored solver path
        solverPath: list[tuple[Coordinates3D, bool]] = self.m_solver.getSolverPath()
        # if no path, then just return
        if len(solverPath) == 0:
            return
        
        # cells that are backtrackers, used to help determine the colour fill of it.
        list_of_backtrackers = [pathElement[0] for pathElement in solverPath if pathElement[1]]

        # Keeps track of how many circles have been drawn
        circle_num = 0

        # pixel shift at each level
        (shiftX, shiftY) = self.m_levelAdjust[solverPath[0][0].getLevel()]

        # draw initial circle at entrance
        self.m_ax.add_patch(plt.Circle(((solverPath[0][0].getCol() + 1.5)*self.m_cellSize + shiftX,
                                      (solverPath[0][0].getRow() + 1.5)*self.m_cellSize + shiftY), 0.2*self.m_cellSize,
                                     fc=(0, circle_num/(len(solverPath) - len(list_of_backtrackers)),
                                         0), alpha=0.4))

        # for each subsequent cell, draw it if it isn't a backtracking one
        for i in range(1, solverPath.__len__()):
            if not solverPath[i][1]:
                (shiftX, shiftY) = self.m_levelAdjust[solverPath[i][0].getLevel()]
                circle_num += 1
                self.m_ax.add_patch(plt.Circle(((solverPath[i][0].getCol() + 1.5)*self.m_cellSize + shiftX,
                    (solverPath[i][0].getRow() + 1.5)*self.m_cellSize + shiftY), 0.2*self.m_cellSize,
                    fc = (0, circle_num/(len(solverPath) - len(list_of_backtrackers)), 0), alpha = 0.4))


    
    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure

        height = sum([7*self.m_maze.rowNum(l) / self.m_maze.colNum(l) for l in range(self.m_maze.levelNum())])
        fig = plt.figure(figsize = (15, height))

        # Create the axes
        self.m_ax = plt.axes()

        # Create the gca
        self.m_gca = fig.gca()

        # Set an equal aspect ratio
        self.m_ax.set_aspect("equal")

        # Remove the axes from the figure
        self.m_ax.axes.get_xaxis().set_visible(False)
        self.m_ax.axes.get_yaxis().set_visible(False)

        return fig

