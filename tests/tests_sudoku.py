import unittest
from unittest.mock import Mock
from sudoku import Sudoku, solve
from copy import deepcopy


SOLVEDSUDOKU1 = Sudoku([[2, 3, 1, 5, 9, 8, 7, 4, 6],
                        [8, 5, 4, 1, 6, 7, 2, 9, 3],
                        [6, 7, 9, 2, 3, 4, 1, 8, 5],
                        [1, 2, 3, 6, 8, 9, 5, 7, 4],
                        [5, 4, 6, 7, 1, 2, 8, 3, 9],
                        [9, 8, 7, 3, 4, 5, 6, 1, 2],
                        [3, 6, 8, 9, 2, 1, 4, 5, 7],
                        [7, 1, 2, 4, 5, 3, 9, 6, 8],
                        [4, 9, 5, 8, 7, 6, 3, 2, 1]])

SUDOKU1 = Sudoku([[2, 3, 1, 5, 9, 8, 7, 4, 0],
                  [8, 5, 4, 1, 6, 7, 2, 9, 3],
                  [6, 7, 9, 2, 3, 4, 1, 8, 5],
                  [1, 2, 3, 6, 8, 9, 5, 7, 4],
                  [5, 4, 6, 7, 1, 2, 8, 3, 9],
                  [9, 8, 7, 3, 4, 5, 6, 1, 2],
                  [3, 6, 8, 9, 2, 1, 4, 5, 7],
                  [7, 1, 2, 4, 5, 3, 9, 6, 8],
                  [4, 9, 5, 8, 7, 6, 3, 2, 1]])

SOLVEDSUDOKU2 = Sudoku([[1, 3, 2, 4, 5, 6, 8, 7, 9],
                        [4, 6, 8, 1, 7, 9, 2, 3, 5],
                        [5, 7, 9, 2, 3, 8, 1, 4, 6],
                        [2, 1, 3, 5, 4, 7, 6, 9, 8],
                        [6, 4, 5, 8, 9, 1, 3, 2, 7],
                        [8, 9, 7, 6, 2, 3, 4, 5, 1],
                        [3, 2, 1, 7, 6, 5, 9, 8, 4],
                        [9, 5, 6, 3, 8, 4, 7, 1, 2],
                        [7, 8, 4, 9, 1, 2, 5, 6, 3]])

SUDOKU2 = Sudoku([[1, 3, 2, 4, 5, 6, 8, 7, 9],
                  [4, 6, 8, 1, 7, 9, 2, 3, 5],
                  [5, 7, 9, 2, 3, 8, 1, 4, 6],
                  [2, 1, 3, 5, 4, 7, 6, 9, 8],
                  [6, 0, 5, 8, 9, 0, 3, 2, 7],
                  [8, 9, 7, 6, 2, 3, 4, 5, 1],
                  [3, 2, 1, 7, 6, 5, 9, 8, 4],
                  [9, 5, 6, 3, 8, 4, 7, 1, 2],
                  [7, 8, 4, 9, 1, 2, 5, 6, 3]])


class TestSudoku(unittest.TestCase):
    def test_should_return_i_j_value(self):
        self.assertEqual(SUDOKU1(2,3), 2)
        self.assertEqual(SUDOKU1(0,8), 0)

    def test_should_return_equal_sudoku_on_deepcopy(self):
        self.assertEqual(SUDOKU1, deepcopy(SUDOKU1))

    def test_should_return_not_equal_with_one_change_sudoku(self):
        other = deepcopy(SUDOKU1)
        other.put(4,7,7)
        self.assertNotEqual(SUDOKU1,other)

    def test_should_return_not_equal_on_solved_sudoku(self):
        solve = Mock(return_value=(True,SOLVEDSUDOKU1))
        self.assertNotEqual(SUDOKU1, solve(SUDOKU1)[1])

    def test_should_return_not_equal_sudokus(self):
        self.assertNotEqual(SUDOKU1, SUDOKU2)

    def test_should_return_true_for_valid_boards(self):
        self.assertTrue(SUDOKU1.is_valid_board())
        self.assertTrue(SOLVEDSUDOKU1.is_valid_board())

    def test_should_validate_zero_board(self):
        self.assertTrue(Sudoku())

    def test_should_not_validate_board_with_repeated_elements_column(self):
        r1 = [i for i in range(1,10)]
        r2 = [0,0,0,0,5,0,0,0,9]
        sudoku = Sudoku([r1] + [[0 for _ in range(0,9)] for _ in range(7)] + [r2])
        self.assertFalse(sudoku.is_valid_board())

    def test_should_not_validate_board_with_repeated_elements_in_small_3x3(self):
        r1 = [i for i in range(1,10)]
        r2 = [0,0,1,0,5,0,0,0,9]
        sudoku = Sudoku([r1] + [[0 for _ in range(9)]] +
                        [r2] + [[0 for _ in range(9)] for _ in range(6)])
        self.assertFalse(sudoku.is_valid_board())

    def test_should_not_validate_board_with_repeated_elements_in_row(self):
        sudoku = Sudoku()
        sudoku.put(0,1,1)
        sudoku.put(0,7,1)
        self.assertFalse(sudoku.is_valid_board())

    def test_should_solve_one_missing_tile(self):
        self.assertTrue(solve(SUDOKU1)[0])
        self.assertEqual(SOLVEDSUDOKU1, solve(SUDOKU1)[1])

    def test_should_solve_two_missing_tiles(self):
        self.assertTrue(solve(SUDOKU2)[0])
        self.assertEqual(SOLVEDSUDOKU2, solve(SUDOKU2)[1])

    def test_should_solve_generated_sudoku(self):
        sudoku = Sudoku()
        sudoku.generate("easy")
        self.assertTrue(solve(sudoku)[0])

    def test_should_not_solve_wrong_sudoku(self):
        sudoku = Sudoku()
        sudoku.put(0,1,1)
        sudoku.put(0,7,1)
        self.assertFalse(solve(sudoku)[0])
