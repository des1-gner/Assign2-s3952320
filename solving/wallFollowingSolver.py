from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from random import choice
from collections import deque

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver for 3D mazes that marks the exit upon reaching it.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        # Mark the entrance as used
        self.solverPathAppend(entrance, False)

        # Run recursive backtracking/DFS from entrance
        stack = deque()
        stack.append(entrance)
        visited = set([entrance])
        path = [entrance]

        while stack:
            current_cell = stack[-1]
            if current_cell in maze.getExits():
                # Mark the current cell as the exit point and finalize the path
                self.solverPathAppend(current_cell, True)
                self.solved(entrance, current_cell)
                return

            neighbours = maze.neighbours(current_cell)
            non_visited_neighs = [neigh for neigh in neighbours if neigh not in visited and not maze.hasWall(current_cell, neigh)]
            if non_visited_neighs:
                next_cell = choice(non_visited_neighs)
                stack.append(next_cell)
                visited.add(next_cell)
                path.append(next_cell)
                self.solverPathAppend(next_cell, False)
            else:
                stack.pop()
                if path:
                    current_cell = path[-1]
                self.solverPathAppend(current_cell, True)

        # Ensure we are currently at the exit
        if current_cell in maze.getExits():
            self.solved(entrance, current_cell)
