from cell import Cell
import random
from time import sleep

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []
        self._win = win

        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        # i is the row index, j is the column index
        # calculate cell_size
        # x1, y1 is the top left corner of the cell
        # x2, y2 is the bottom right corner of the cell
        # calculate x1
        x1 = self._x1 + j * self._cell_size_x
        # calculate y1
        y1 = self._y1 + i * self._cell_size_y
        # calculate x2
        x2 = x1 + self._cell_size_x
        # calculate y2
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        # draw the cell
        self._animate()

    def _break_entrance_and_exit(self):
        # break the entrance and exit walls
        # entrance is the top left corner of the maze
        # exit is the bottom right corner of the maze
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        # Mark the current cell as visited
        self._cells[i][j].visited = True

        while True:
            # Create a list to hold possible directions
            possible_directions = []

            # Check adjacent cells
            if i > 0 and not self._cells[i - 1][j].visited:  # Up
                possible_directions.append((-1, 0))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:  # Down
                possible_directions.append((1, 0))
            if j > 0 and not self._cells[i][j - 1].visited:  # Left
                possible_directions.append((0, -1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:  # Right
                possible_directions.append((0, 1))

            # If no directions are possible, draw the cell and return
            if not possible_directions:
                self._draw_cell(i, j)
                return

            # Pick a random direction
            di, dj = random.choice(possible_directions)

            # Knock down the wall between the current cell and the chosen cell
            if di == -1:  # Up
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
            elif di == 1:  # Down
                self._cells[i][j].has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
            elif dj == -1:  # Left
                self._cells[i][j].has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
            elif dj == 1:  # Right
                self._cells[i][j].has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False

            # Move to the chosen cell
            self._break_walls_r(i + di, j + dj)

    def _reset_cells_visited(self):
      for col in self._cells:
          for cell in col:
              cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        # Call the _animate method
        self._animate()

        # Mark the current cell as visited
        self._cells[i][j].visited = True

        # If you are at the "end" cell (bottom-right corner), return True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # Define possible directions: (di, dj) for Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for di, dj in directions:
            ni, nj = i + di, j + dj

            # Check if the next cell is within bounds, has no wall blocking, and hasn't been visited
            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows and not self._cells[ni][nj].visited:
                if (di == -1 and not self._cells[i][j].has_top_wall) or \
                    (di == 1 and not self._cells[i][j].has_bottom_wall) or \
                    (dj == -1 and not self._cells[i][j].has_left_wall) or \
                    (dj == 1 and not self._cells[i][j].has_right_wall):

                    # Draw a move between the current cell and the next cell
                    self._cells[i][j].draw_move(self._cells[ni][nj])

                    # Recursively call _solve_r to move to the next cell
                    if self._solve_r(ni, nj):
                        return True

                    # If the move didn't work out, draw an "undo" move
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)

        # If none of the directions worked out, return False
        return False

    def _animate(self):
        if self._win is None:
            return
        # animate the cell by calling the redraw method from self._win
        self._win.redraw()
        sleep(0.05)