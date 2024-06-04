# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wilson's algorithm maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator

# Imported libraries
from random import randint, choice
from collections import deque


class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """

    def getRandCoordinate(
        self, method: str, maze: Maze3D, finalised: set[Coordinates3D]
    ):
        """
        Gets a random coordinate from the maze that is not finalised. There are two methods to getting a \
        random coordinate: 
        - loop - where a coordinate is randomly generated until it is not finalised;
        - sets - where all coordinates are considered and then removed by the finalised set.
        """
        if method == "loop":
            while True:
                selectedRandomLevel = randint(0, maze.levelNum() - 1)
                selectedCoord = Coordinates3D(
                    selectedRandomLevel,
                    randint(0, maze.rowNum(selectedRandomLevel) - 1),
                    randint(0, maze.colNum(selectedRandomLevel) - 1),
                )
                if selectedCoord not in finalised:
                    return selectedCoord
        elif method == "sets":
            # generate all possible coordinates in the maze
            all_coords = [
                Coordinates3D(level, row, col)
                for level in range(maze.levelNum())
                for row in range(maze.rowNum(level))
                for col in range(maze.colNum(level))
            ]
            # find coordinates that are not finalised
            non_finalised_coords = [
                coord for coord in all_coords if coord not in finalised
            ]
            return choice(non_finalised_coords)
        else:
            return

    def generateMaze(self, maze: Maze3D):
        # TODO: Implement this method for task A.
        # make sure we start the maze with all walls there
        maze.initCells(True)

        # select starting cell
        # random floor
        startRandomLevel = randint(0, maze.levelNum() - 1)
        startCoord: Coordinates3D = Coordinates3D(
            startRandomLevel,
            randint(0, maze.rowNum(startRandomLevel) - 1),
            randint(0, maze.colNum(startRandomLevel) - 1),
        )

        # finalised set instead of visited, for distinction between random walks and carved paths
        finalised: set[Coordinates3D] = set([startCoord])

        totalCells = sum(
            [maze.rowNum(l) * maze.colNum(l) for l in range(maze.levelNum())]
        )

        # threshold for switching methods for finding a random node
        threshold = totalCells // 2

        while len(finalised) < totalCells:
            # pick a random coordinate that is not already finalised
            if len(finalised) < threshold:
                selectedCoord = self.getRandCoordinate("loop", maze, finalised)
            else:
                selectedCoord = self.getRandCoordinate("sets", maze, finalised)

            # deque that holds coordinates in random walk
            walk: deque[Coordinates3D] = deque([selectedCoord])
            # perform walk with randomly selected cell, which stops when it visits a cell that is finalised
            currCell: Coordinates3D = selectedCoord
            while currCell not in finalised:
                neighbours: list[Coordinates3D] = maze.neighbours(currCell)

                possibleNeighs: list[Coordinates3D] = [
                    neigh
                    for neigh in neighbours
                    if not maze.isBoundary(neigh)
                    and (neigh.getRow() >= -1)
                    and (neigh.getRow() <= maze.rowNum(neigh.getLevel()))
                    and (neigh.getCol() >= -1)
                    and (neigh.getCol() <= maze.colNum(neigh.getLevel()))
                ]
                selectedNeighs = choice(possibleNeighs)
                # if selected node is already in walk, then a loop has formed - backtrack the walk to the already visited node
                if selectedNeighs in walk:
                    # begin backtrack
                    backtrackedCell = walk.pop()
                    # back track to selectedNeigh (which is already in the walk)
                    while backtrackedCell != selectedNeighs:
                        backtrackedCell = walk.pop()
                # push or re-push node that was already in the walk
                walk.append(selectedNeighs)
                currCell = selectedNeighs
            # loop exits when currCell visits a finalised node

            # first cell in walk will always be the finalised cell
            finalisedCell = walk.pop()
            # now back track walk to selected coordinate (beginning of walk), removing walls along the way (creating a path)
            while walk:
                currCell = walk.pop()
                maze.removeWall(finalisedCell, currCell)
                # add cells to finalised set
                finalised.add(finalisedCell)
                finalised.add(currCell)
                finalisedCell = currCell
        self.m_mazeGenerated = True
