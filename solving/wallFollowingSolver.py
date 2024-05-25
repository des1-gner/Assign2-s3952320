from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation for a 3D maze.
    """
    def __init__(self):
        super().__init__()
        self.m_name = "wall"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False

        # Define the order of directions for rotation (right-hand rule)
        directions = [
            Coordinates3D(0, -1, 0),      # North
            Coordinates3D(1, -1, 0),      # North-East (up one level)
            Coordinates3D(1, 0, 0),       # East
            Coordinates3D(1, 1, 0),       # South-East (up one level)
            Coordinates3D(0, 1, 0),       # South
            Coordinates3D(-1, 1, 0),      # South-West (down one level)
            Coordinates3D(-1, 0, 0),      # West
            Coordinates3D(-1, -1, 0),     # North-West (down one level)
            Coordinates3D(0, 0, 1),       # Up
            Coordinates3D(0, 0, -1)      # Down
        ]

        # Set the initial direction to East
        direction_index = 2  # Start facing East
        # Set the current cell to the entrance
        current_cell = entrance
        # Initialize the path with the entrance cell
        self.solverPathAppend(current_cell, False)
        # Stack to manage the path for backtracking
        path_stack = [(current_cell, direction_index)]
        # Set of visited cells to detect loops
        visited_cells = set()
        visited_cells.add(current_cell)

        # Helper function to turn right relative to the current direction
        def turn_right(index):
            return (index + 1) % len(directions)

        # Helper function to turn left relative to the current direction
        def turn_left(index):
            return (index - 1) % len(directions)

        # Helper function to check if a cell is within maze bounds
        def is_within_bounds(cell):
            level = cell.getLevel()
            levels = maze.levelNum()
            if not (0 <= level < levels):
                return False
            rows = maze.rowNum(level)
            cols = maze.colNum(level)
            return (0 <= cell.getRow() < rows and 0 <= cell.getCol() < cols)

        while current_cell not in maze.getExits():
            print(f"Current cell: {current_cell}, Direction index: {direction_index}")

            # Check all primary directions (right, forward, left) in sequence
            left_direction_index = turn_left(direction_index)
            right_direction_index = turn_right(direction_index)

            # Determine the potential next cells
            left_cell = current_cell + directions[left_direction_index]
            forward_cell = current_cell + directions[direction_index]
            right_cell = current_cell + directions[right_direction_index]

            print(f"Checking cells: Left {left_cell}, Forward {forward_cell}, Right {right_cell}")

            moved = False

            # Try to turn right and move if possible
            if (is_within_bounds(right_cell) and maze.hasCell(right_cell) and 
                not maze.hasWall(current_cell, right_cell) and 
                right_cell not in visited_cells):
                print(f"Moving right to {right_cell}")
                current_cell = right_cell
                direction_index = right_direction_index
                moved = True
            # Otherwise, try to move forward
            elif (is_within_bounds(forward_cell) and maze.hasCell(forward_cell) and 
                  not maze.hasWall(current_cell, forward_cell) and 
                  forward_cell not in visited_cells):
                print(f"Moving forward to {forward_cell}")
                current_cell = forward_cell
                moved = True
            # Try to turn left and move if possible
            elif (is_within_bounds(left_cell) and maze.hasCell(left_cell) and 
                  not maze.hasWall(current_cell, left_cell) and 
                  left_cell not in visited_cells):
                print(f"Moving left to {left_cell}")
                current_cell = left_cell
                direction_index = left_direction_index
                moved = True
            # Try to move upwards if possible
            elif (is_within_bounds(current_cell + directions[8]) and maze.hasCell(current_cell + directions[8]) and 
                  not maze.hasWall(current_cell, current_cell + directions[8]) and 
                  current_cell + directions[8] not in visited_cells):
                print(f"Moving up to {current_cell + directions[8]}")
                current_cell += directions[8]
                moved = True
            # Try to move downwards if possible
            elif (is_within_bounds(current_cell + directions[9]) and maze.hasCell(current_cell + directions[9]) and 
                  not maze.hasWall(current_cell, current_cell + directions[9]) and 
                  current_cell + directions[9] not in visited_cells):
                print(f"Moving down to {current_cell + directions[9]}")
                current_cell += directions[9]
                moved = True

            if moved:
                # Append the current cell to the path and mark it as visited
                self.solverPathAppend(current_cell, False)
                visited_cells.add(current_cell)
                path_stack.append((current_cell, direction_index))
            else:
                # If no move is possible, backtrack
                print("Backtracking")
                if len(path_stack) > 1:
                    path_stack.pop()  # Remove the current cell
                    current_cell, direction_index = path_stack[-1]
                    self.solverPathAppend(current_cell, True)
                else:
                    break

            # Check if we have found the exit
            if current_cell in maze.getExits():
                self.solved(entrance, current_cell)
                self.m_solved = True
                print("Exit found!")
                break

            print(f"Visited cells: {visited_cells}")

        if not self.m_solved:
            self.m_solved = False
            print("No solution found.")

