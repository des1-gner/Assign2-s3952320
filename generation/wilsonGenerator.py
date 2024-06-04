# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wilson's algorithm maze generator.
#
# __author__ = 'Jeffrey Chan', 'Oisin Aeonn'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

# Imported Libraries

from random import randint, choice
from collections import deque

class WilsonMazeGenerator(MazeGenerator):

    """
    Wilson algorithm maze generator.
    TODO: Complete the implementation (Task A)
    Done :)
    """

    # Gets a random coordinate from the maze that is not finalised
    
    def getRandCoordinate(self, method: str, maze: Maze3D, finalised: set[Coordinates3D]):
        
        # Method using a loop to find a non-finalised coordinate
    
        if method == "loop":
    
            while True:
    
                selectedRandomLevel = randint(0, maze.levelNum() - 1)
                selectedCoord = Coordinates3D(
    
                    selectedRandomLevel,
                    randint(0, maze.rowNum(selectedRandomLevel) - 1),
                    randint(0, maze.colNum(selectedRandomLevel) - 1),
    
                )
                
                # Return unfinalised coordinate
    
                if selectedCoord not in finalised:
    
                    return selectedCoord
                    
        # Method using sets to find a non-finalised coordinate
    
        elif method == "sets":
    
            all_coords = [
    
                Coordinates3D(level, row, col)
    
                for level in range(maze.levelNum())
                for row in range(maze.rowNum(level))
                for col in range(maze.colNum(level))
    
            ]
    
            non_finalised_coords = [coord for coord in all_coords if coord not in finalised]
    
            return choice(non_finalised_coords)
        
        else:
    
            return None

    # Perform a random walk starting from startCoord until a finalised cell is reached
    
    def performRandomWalk(self, maze: Maze3D, startCoord: Coordinates3D, finalised: set[Coordinates3D]):
        
        walk: deque[Coordinates3D] = deque([startCoord])
        currCell: Coordinates3D = startCoord
        
        while currCell not in finalised:
        
            neighbours: list[Coordinates3D] = maze.neighbours(currCell)
            possibleNeighs: list[Coordinates3D] = [
        
                neigh for neigh in neighbours
        
                if not maze.isBoundary(neigh)
                and 0 <= neigh.getRow() < maze.rowNum(neigh.getLevel())
                and 0 <= neigh.getCol() < maze.colNum(neigh.getLevel())
        
            ]
        
            if not possibleNeighs:
        
                break  # Exit if no valid neighbours (shouldn't happen in a valid maze)

            selectedNeigh = choice(possibleNeighs)
        
            if selectedNeigh in walk:
        
                # Loop detected, backtrack to remove loop
        
                while walk.pop() != selectedNeigh:
        
                    pass
        
                walk.append(selectedNeigh)
        
            else:
        
                walk.append(selectedNeigh)
        
            currCell = selectedNeigh
        
        return walk

    # Generates the maze using Wilson's algorithm.

    def generateMaze(self, maze: Maze3D):
        
        maze.initCells(True)

        # Select a random starting coordinate and mark it as finalised
        
        startRandomLevel = randint(0, maze.levelNum() - 1)
        startCoord = Coordinates3D(
        
            startRandomLevel,
            randint(0, maze.rowNum(startRandomLevel) - 1),
            randint(0, maze.colNum(startRandomLevel) - 1),
        
        )

        finalised: set[Coordinates3D] = {startCoord}

        # Total number of cells in the maze
        
        totalCells = sum(maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum()))
        threshold = totalCells // 2

        while len(finalised) < totalCells:
        
            # Choose method based on the number of finalised cells
        
            selectedCoord = self.getRandCoordinate("loop" if len(finalised) < threshold else "sets", maze, finalised)
            walk = self.performRandomWalk(maze, selectedCoord, finalised)

            finalisedCell = walk.pop()
        
            # Finalise the cells and remove walls between them
        
            while walk:
        
                currCell = walk.pop()
                maze.removeWall(finalisedCell, currCell)
                finalised.add(finalisedCell)
                finalised.add(currCell)
                finalisedCell = currCell

        self.m_mazeGenerated = True
