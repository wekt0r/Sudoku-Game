from random import randint, choice, choices
from collections import defaultdict, deque
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

    def cp(self):
        """Make fast copy of sudoku."""
        return Sudoku([list(row) for row in self.board])


def solve(sudoku):
    """
    Check if sudoku has solution and return this solution.
    """
    to_fill = [(i, j) for i in range(0, 9) for j in range(0, 9)
               if sudoku.board[i][j] == 0]
    return _solve(sudoku.cp(), to_fill)


def _is_valid_line(line):
    return all(line.count(i) <= 1 for i in range(1, 10))


def _solve(starting_sudoku, starting_to_fill):
    stack = deque([(starting_sudoku, starting_to_fill)])
    while stack:
        sudoku, to_fill = stack.pop()
        if not to_fill and sudoku.is_valid_board():
            return True, sudoku
        if to_fill and sudoku.is_valid_board():
            [(i,j), *rest_to_fill] = to_fill
            for val in range(1,10):
                new_sudoku = sudoku.cp()
                new_sudoku.put(i,j,val)
                stack.append((new_sudoku, rest_to_fill))
    return False, starting_sudoku


def _transpose(matrix):
    return [[matrix[j][i] for j in range(9)] for i in range(9)]


def _get_3x3s(matrix):
    return [[matrix[j+dj][i+di] for dj in [0, 1, 2] for di in [0, 1, 2]]
            for i in [0, 3, 6] for j in [0, 3, 6]]
