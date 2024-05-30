from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation for 3D mazes.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"

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
        current_direction_index = 0  # Start with a fixed direction (South)
        angle = 0
        visited = set()
        path = [current_cell]

        def is_within_bounds(cell):
            return maze.hasCell(cell)

        def turn_left():
            nonlocal current_direction_index, angle
            current_direction_index = (current_direction_index - 1) % len(directions)
            angle += 90

        def turn_right():
            nonlocal current_direction_index, angle
            current_direction_index = (current_direction_index + 1) % len(directions)
            angle -= 90

        def move_forward():
            nonlocal current_cell
            next_cell = current_cell + directions[current_direction_index]
            if is_within_bounds(next_cell) and not maze.hasWall(current_cell, next_cell):
                current_cell = next_cell
                path.append(current_cell)
                return True
            return False

        while True:
            if current_cell in maze.getExits() and current_cell != entrance:
                self.solverPathAppend(current_cell, True)
                self.solved(entrance, current_cell)
                return

            if current_cell not in visited:
                visited.add(current_cell)
                self.solverPathAppend(current_cell, False)

            if move_forward():
                angle = 0  # Reset angle when moving forward without obstacles
            else:
                turn_left()  # Start with a left turn if unable to move forward

            while angle != 0:
                if move_forward():
                    break  # Exit the while loop if we can move forward
                turn_right()  # Turn right if unable to move forward

            # Prevent getting stuck in a loop or revisiting the entrance unnecessarily
            if not move_forward() and angle == 0:
                if len(path) > 1:
                    path.pop()
                    current_cell = path[-1]
                else:
                    self.m_solved = False
                    return

        # Ensure the solver path is appended correctly
        path.append(current_cell)

