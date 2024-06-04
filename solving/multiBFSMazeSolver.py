from collections import deque
from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class MultiBFSMazeSolver(MazeSolver):
    """
    Multi-Source BFS solver implementation.
    """
    def __init__(self):
        super().__init__()
        self.m_name = "multi_bfs"

    def solveMaze(self, maze: Maze3D, entrances: Coordinates3D | list[Coordinates3D]):
        self.m_solved = False
        queue = deque()
        visited = set()
        parent_map = {}

        # Ensure entrances is a list
        if isinstance(entrances, Coordinates3D):
            entrances = [entrances]

        # Add all entrance cells to the queue
        for entrance in entrances:
            queue.append((entrance, 0))  # (cell, distance)
            visited.add(entrance)
            self.solverPathAppend(entrance, False)
            parent_map[entrance] = None

        while queue:
            currCell, dist = queue.popleft()
            # Check if the current cell is an exit
            if currCell in maze.getExits():
                self.solved(entrances, currCell, parent_map)
                return

            # Get all valid neighbors of the current cell
            neighbors = maze.neighbours(currCell)
            for neigh in neighbors:
                if (neigh not in visited and 
                    not maze.hasWall(currCell, neigh) and
                    0 <= neigh.getRow() < maze.rowNum(neigh.getLevel()) and
                    0 <= neigh.getCol() < maze.colNum(neigh.getLevel())):
                    queue.append((neigh, dist + 1))
                    visited.add(neigh)
                    self.solverPathAppend(neigh, False)
                    parent_map[neigh] = currCell

        # If no exit was found
        self.m_solved = False

    def solved(self, entrances: list[Coordinates3D], exit: Coordinates3D, parent_map):
        self.m_solved = True
        print(f"Maze solved! Exit found at {exit}.")
        self.solverPathAppend(exit, True)

        # Trace back the path from exit to entrance
        path = []
        curr = exit
        while curr is not None:
            path.append(curr)
            curr = parent_map[curr]

        # Reverse the path to start from the entrance
        path.reverse()

        # Mark the path in the maze
        for cell in path:
            self.solverPathAppend(cell, cell == exit)

        entrance = path[0]
        print(f"Solver used Entrance {entrance} and Exit {exit}.")

# No example usage in the module to keep it clean.

