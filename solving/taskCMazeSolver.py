from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from collections import deque, defaultdict
import heapq

class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation. You'll need to complete its implementation for task C.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"

    def solveMaze(self, maze: Maze3D):
        """
        solve the maze, used by Task C.
        This version of solveMaze does not provide a starting entrance, and as part of the solution, the method should
        find the entrance and exit pair (see project specs for requirements of this task).
        """
        entrances = maze.getEntrances()
        exits = []
        explored_cells_count = defaultdict(int)

        # Exploration Phase: Discover exits from each entrance
        for entrance in entrances:
            self.exploreFromEntrance(maze, entrance, exits, explored_cells_count)

        if len(exits) == 0:
            raise ValueError("No exits found during exploration phase.")

        # Distance Calculation Phase
        min_cost = float('inf')
        best_entrance_exit_pair = None
        best_path = []

        for entrance in entrances:
            for exit in exits:
                cost, path = self.calculateCostAndPath(maze, entrance, exit, explored_cells_count[entrance])
                if cost < min_cost:
                    min_cost = cost
                    best_entrance_exit_pair = (entrance, exit)
                    best_path = path

        # Mark the best path in the maze
        for cell in best_path:
            self.solverPathAppend(cell, False)
        self.solverPathAppend(best_entrance_exit_pair[1], True)
        self.solved(best_entrance_exit_pair[0], best_entrance_exit_pair[1])

        # Determine if further exploration was worthwhile
        total_explored_cells = sum(explored_cells_count.values())
        print(f"Total cells explored: {total_explored_cells}")
        print(f"Best path cost (cells explored + distance): {min_cost}")

    def exploreFromEntrance(self, maze, entrance, exits, explored_cells_count):
        queue = deque([entrance])
        visited = set()
        visited.add(entrance)
        while queue:
            current_cell = queue.popleft()
            explored_cells_count[entrance] += 1
            if current_cell in maze.m_exit:  # Adjusted to check for exits correctly
                exits.append(current_cell)
            for direction in [Coordinates3D(0, 1, 0), Coordinates3D(0, 0, 1), Coordinates3D(0, -1, 0), Coordinates3D(0, 0, -1), Coordinates3D(1, 0, 0), Coordinates3D(-1, 0, 0)]:
                next_cell = current_cell + direction
                if maze.hasCell(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                    visited.add(next_cell)
                    queue.append(next_cell)

    def calculateCostAndPath(self, maze, entrance, exit, initial_explored_cells_count):
        # Use Dijkstra's algorithm to find the shortest path from entrance to exit
        pq = [(0, entrance, [])]  # (cost, current_cell, path)
        visited = set()
        total_explored_cells = initial_explored_cells_count

        while pq:
            cost, current_cell, path = heapq.heappop(pq)
            if current_cell in visited:
                continue
            visited.add(current_cell)
            new_path = path + [current_cell]
            if current_cell == exit:
                return cost + total_explored_cells, new_path
            for direction in [Coordinates3D(0, 1, 0), Coordinates3D(0, 0, 1), Coordinates3D(0, -1, 0), Coordinates3D(0, 0, -1), Coordinates3D(1, 0, 0), Coordinates3D(-1, 0, 0)]:
                next_cell = current_cell + direction
                if maze.hasCell(next_cell) and not maze.hasWall(current_cell, next_cell) and next_cell not in visited:
                    heapq.heappush(pq, (cost + 1, next_cell, new_path))
                    total_explored_cells += 1
        return float('inf'), []  # If no path is found

