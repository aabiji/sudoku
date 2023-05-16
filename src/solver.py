class Cell():
    def __init__(self):
        self.val = 0
        self.x, self.y = 0, 0
        self.blockx, self.blocky = 0, 0
        self.fixed = False

    def load(self, x: int, y: int, digit: int):
        self.val = digit        
        self.x, self.y = x, y
        self.blockx, self.blocky  = int(x / 3), int(y / 3)
        self.fixed = True if digit != 0 else False

class Solver():
    def __init__(self, initial_board):
        self.board = initial_board

    def  __repr__(self):
        out = ""
        for y in range(9):
            for x in range(9):
                out += f"{self.board[y][x].val} "
            out += "\n"
        out += "--------------------\n"
        return out

    def is_valid(self, cell: Cell) -> bool:
        for x in range(9):
            if self.board[cell.y][x] == cell.val:
                return False

        for y in range(9):
            if self.board[y][cell.x] == cell.val:
                return False

        for y in range(3):
            for x in range(3):
                if self.board[cell.blocky + y][cell.blockx + x].val == cell.val:
                    return False

        return True

    def get_value(self, cell: Cell) -> Cell:
        for i in range(cell.val, 9):
            cell.val = i
            if self.is_valid(cell):
                return cell

        cell.val = 0
        return cell # No match found

    # Solving the sudoku board using backtracking
    # https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
    def solve_sudoku(self):
        pass