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
        # Directions corresponding to [South, East, North, West, Up, Down]
        directions = [
            Coordinates3D(0, 1, 0),   # South
            Coordinates3D(0, 0, 1),   # East
            Coordinates3D(0, -1, 0),  # North
            Coordinates3D(0, 0, -1),  # West
            Coordinates3D(1, 0, 0),   # Up (to next level)
            Coordinates3D(-1, 0, 0)   # Down (to previous level)
        ]

        def right_wall_dirs(current_dir):
            # Returns direction order based on current direction
            if current_dir == Coordinates3D(0, 1, 0):   # South
                return [1, 0, 3, 2, 4, 5]  # East, South, West, North, Up, Down
            elif current_dir == Coordinates3D(0, 0, 1):  # East
                return [0, 1, 2, 3, 4, 5]  # South, East, North, West, Up, Down
            elif current_dir == Coordinates3D(0, -1, 0): # North
                return [3, 2, 1, 0, 4, 5]  # West, North, East, South, Up, Down
            elif current_dir == Coordinates3D(0, 0, -1): # West
                return [2, 3, 0, 1, 4, 5]  # North, West, South, East, Up, Down
            elif current_dir == Coordinates3D(1, 0, 0):  # Up
                return [0, 1, 2, 3, 4, 5]  # South, East, North, West, Up, Down
            elif current_dir == Coordinates3D(-1, 0, 0): # Down
                return [0, 1, 2, 3, 5, 4]  # South, East, North, West, Down, Up

        current_cell = entrance
        current_dir = Coordinates3D(0, 1, 0)  # Start facing South
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
            for dir_index in right_wall_dirs(current_dir):
                next_dir = directions[dir_index]
                next_cell = current_cell + next_dir

                # Check if the next cell is an exit or a valid step
                if (next_cell in maze.getExits() or 
                    (maze.hasCell(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited)):
                    current_cell = next_cell
                    current_dir = next_dir
                    path.append(current_cell)
                    found_path = True
                    break

            if not found_path:
                path.pop()  # Remove current position
                if path:
                    current_cell = path[-1]
                self.solverPathAppend(current_cell, True)

        self.solved(entrance, current_cell)

