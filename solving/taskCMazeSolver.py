from random import choices
from collections import deque, defaultdict
from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation using a biased DFS algorithm.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False

        # select starting cell
        startCoord: Coordinates3D = entrance

        # run biased DFS from starting cell
        stack: deque = deque([startCoord])
        currCell: Coordinates3D = startCoord
        visited: set[Coordinates3D] = set([startCoord])
        visit_count: defaultdict[Coordinates3D, int] = defaultdict(int)

        visit_count[startCoord] += 1
        self.solverPathAppend(startCoord, False)

        while stack:
            currCell = stack[-1]
            # find all neighbors of current cell
            neighbors: list[Coordinates3D] = maze.neighbours(currCell)

            # filter to ones that haven't been visited and within boundary and doesn't have a wall between them
            nonVisitedNeighs: list[Coordinates3D] = [
                neigh for neigh in neighbors
                if neigh not in visited and not maze.hasWall(currCell, neigh)
            ]

            # see if any unvisited neighbors
            if nonVisitedNeighs:
                # bias towards less explored regions
                weights = [1 / (self.regionExplorationWeight(maze, neigh, visit_count) + 1) for neigh in nonVisitedNeighs]
                total_weight = sum(weights)
                probabilities = [weight / total_weight for weight in weights]
                neigh = choices(nonVisitedNeighs, probabilities)[0]

                # add to stack
                stack.append(neigh)

                # update visited and visit count
                visited.add(neigh)
                visit_count[neigh] += 1
                self.solverPathAppend(neigh, False)

                # update currCell
                currCell = neigh
            else:
                # backtrack
                stack.pop()
                if stack:
                    currCell = stack[-1]
                    self.solverPathAppend(currCell, True)
                else:
                    break

            if currCell in maze.getExits():
                self.solved(entrance, currCell)
                return

    def regionExplorationWeight(self, maze: Maze3D, cell: Coordinates3D, visit_count: defaultdict) -> int:
        """
        Calculate the exploration weight of a cell based on the visit counts of its neighboring regions.
        """
        directions = [
            Coordinates3D(0, 1, 0), Coordinates3D(0, 0, 1),
            Coordinates3D(0, -1, 0), Coordinates3D(0, 0, -1),
            Coordinates3D(1, 0, 0), Coordinates3D(-1, 0, 0)
        ]
        weight = 0
        for direction in directions:
            neighbor = cell + direction
            if maze.hasCell(neighbor) and not maze.hasWall(cell, neighbor):
                weight += visit_count[neighbor]
        return weight

    def getNeighbors(self, maze, cell):
        directions = [
            Coordinates3D(0, 1, 0), Coordinates3D(0, 0, 1),
            Coordinates3D(0, -1, 0), Coordinates3D(0, 0, -1),
            Coordinates3D(1, 0, 0), Coordinates3D(-1, 0, 0)
        ]
        neighbors = [cell + direction for direction in directions if maze.hasCell(cell + direction) and not maze.hasWall(cell, cell + direction)]
        return neighbors

    def getInitialDirectionIndex(self, entrance, maze):
        """
        Determines the initial direction index to move into the maze based on the entrance position.
        """
        level, row, col = entrance.getLevel(), entrance.getRow(), entrance.getCol()

        # Check the position relative to the maze boundaries to determine the direction
        if col < 0:  # Entrance is to the left of the maze
            return 1  # Move East
        elif col >= maze.colNum(level):  # Entrance is to the right of the maze
            return 3  # Move West
        elif row < 0:  # Entrance is below the maze
            return 0  # Move North
        elif row >= maze.rowNum(level):  # Entrance is above the maze
            return 2  # Move South
        
        raise ValueError("Entrance is not valid")

    def markPath(self, entrance, exit, path):
        for cell in path:
            self.solverPathAppend(cell, False)
        self.solverPathAppend(exit, True)
        self.solved(entrance, exit)

