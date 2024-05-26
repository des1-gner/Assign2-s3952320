from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver for 3D mazes that marks the exit upon reaching it.
    """
    def __init__(self):
        super().__init__()
        self.m_name = "wall"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        directions = [
            Coordinates3D(0, 1, 0),   # South
            Coordinates3D(0, 0, 1),   # East
            Coordinates3D(0, -1, 0),  # North
            Coordinates3D(0, 0, -1),  # West
            Coordinates3D(1, 0, 0),   # Up (to next level)
            Coordinates3D(-1, 0, 0)   # Down (to previous level)
        ]

        current_cell = entrance
        current_dir_index = 0  # Start facing South
        visited = set()
        path = [current_cell]

        while True:
            visited.add(current_cell)
            self.solverPathAppend(current_cell, False)

            if current_cell in maze.getExits():
                # Mark the current cell as the exit point and finalize the path
                self.solverPathAppend(current_cell, True)
                break

            found_path = False
            attempts = 0
            while attempts < len(directions):
                next_dir = directions[current_dir_index]
                next_cell = current_cell + next_dir

                # Check if the next cell is an exit or a valid step
                if (next_cell in maze.getExits() or 
                    (not maze.hasWall(current_cell, next_cell) and next_cell not in visited and maze.hasCell(next_cell))):
                    current_cell = next_cell
                    path.append(current_cell)
                    found_path = True
                    break
                else:
                    current_dir_index = (current_dir_index + 1) % len(directions)
                    attempts += 1

            if not found_path:
                path.pop()  # Remove current position
                if path:
                    current_cell = path[-1]
                self.solverPathAppend(current_cell, True)

        self.solved(entrance, current_cell)


