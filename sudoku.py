from random import randint, choice, choices
from copy import deepcopy
from collections import defaultdict
from multiprocessing.pool import ThreadPool


class Sudoku:
    """Represents Sudoku."""

    def __init__(self, board=None):
        self.board = board if board else [[0]*9 for _ in range(9)]

    def __call__(self, i, j):
        """Return value in i-th row in j-th column of sudoku."""
        return self.board[i][j]

    def __eq__(self, other):
        """Check whether two Sudokus has same entries."""
        return all(self.board[i] == other.board[i] for i in range(0, 9))

    def put(self, i, j, value):
        """Set value on intersection of i-th row and j-th column."""
        try:
            self.board[i][j] = int(value)
        except ValueError:
            print("WARNING: Tried to put {} on {},{}".format(value, i, j))

    def is_valid_board(self):
        """Check if sudoku is valid in terms of rules of classical sudoku."""
        return (all(_is_valid_line(row)
                    for row in self.board)
                and all(_is_valid_line(column)
                        for column in _transpose(self.board))
                and all(_is_valid_line(threex3)
                        for threex3 in _get_3x3s(self.board)))

    def generate(self, difficulty):
        generator = ThreadPool(processes=1)
        generated = generator.apply_async(self._generate, (difficulty,))
        self.board = generated.get()

    @staticmethod
    def _generate(difficulty):
        """
        Generate random board of chosen difficulty.

        Difficulties are "really hard", "hard", "medium" or "easy".
        """
        generated = Sudoku()
        tiles_amount = {"really hard": 17,
                        "hard": choice(range(18, 22)),
                        "medium": choice(range(22, 26)),
                        "easy": choice(range(26, 30))}[difficulty]
        fillable = [(i, j) for i in range(0, 9) for j in range(0, 9)]
        first_square = [(i, j) for i in range(0, 2) for j in range(0, 2)]
        filled = []
        k = 0
        while 0 <= k < 3:
        #    print(first_square)
            i, j = choice(first_square)
            generated.put(i, j, randint(1, 9))
            if generated.is_valid_board() and solve(generated)[0]:
                k += 1
                first_square.remove((i, j))
                filled.append((i, j))
            else:
                k -= 1
                generated.put(i, j, 0)
                first_square.append((i, j))

        k = 0
        while 0 <= k < 5:
            i, j = choice(fillable)
            generated.put(i, j, randint(1, 9))
            if generated.is_valid_board() and solve(generated)[0]:
                k += 1
                fillable.remove((i, j))
                filled.append((i, j))
            else:
                k -= 1
                generated.put(i, j, 0)
        #print("we have * \n {} \n".format(self))
        solved = solve(generated)[1]
        generated.board = [[0]*9 for _ in range(9)]
        for i, j in choices([(i, j) for i in range(0, 9) for j in range(0, 9)],
                            k=tiles_amount):
            generated.put(i, j, solved.board[i][j])

        return generated.board

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.board])

    def __deepcopy__(self, memo):
        """Make deepcopy of sudoku."""
        return Sudoku(deepcopy(self.board))


def solve(sudoku):
    """
    Check if sudoku has solution and return this solution.

    Done with multiprocessing.
    """
    to_fill = [(i, j) for i in range(0, 9) for j in range(0, 9)
               if sudoku.board[i][j] == 0]

    solver = ThreadPool(processes=1)
    solution = solver.apply_async(_solve, (deepcopy(sudoku), to_fill))

    return solution.get()


def _is_valid_line(line):
    return all(line.count(i) <= 1 for i in range(1, 10))


def _solve(sudoku, to_fill):
    k = 0
    ks = defaultdict(int)
    while 0 <= k < len(to_fill):
        i, j = to_fill[k]
        for value in range(ks[k] + 1, 10):
            ks[k] = value
            sudoku.board[i][j] = value
            if sudoku.is_valid_board():
                k += 1
                break

        if ks[k] == 9:
            ks[k] = 0
            sudoku.board[i][j] = 0
            k -= 1
    return k == len(to_fill), sudoku


def _transpose(matrix):
    return [[matrix[j][i] for j in range(9)] for i in range(9)]


def _get_3x3s(matrix):
    return [[matrix[j+dj][i+di] for dj in [0, 1, 2] for di in [0, 1, 2]]
            for i in [0, 3, 6] for j in [0, 3, 6]]
