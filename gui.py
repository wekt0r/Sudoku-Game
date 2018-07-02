import pygame
import sys
import random
from sudoku import Sudoku, solve
import pickle

FONT = "images/bebas.ttf"

COLORS = {"blue": pygame.Color(0, 85, 220, 0),
          "lightblue": pygame.Color(120, 180, 255, 0),
          "red": pygame.Color(200, 20, 20, 0),
          "green": pygame.Color(20, 200, 20, 0),
          "black": pygame.Color(0, 0, 0, 0),
          "white": pygame.Color(255, 255, 255, 0)}

MENU_FONT_COLOR = COLORS["white"]

HEIGHT = 650
WIDTH = 400
SUDOKUX, SUDOKUY = 10, HEIGHT - 400
DIFFICULTY = "medium"

NEW_GAME = "NEW GAME"
SOLVE = "SOLVE"
CHECK = "CHECK"
HINT = "HINT!"
LOAD = "LOAD"
SAVE = "SAVE"


class GUI:
    """
    Handle game's interface.

    Use PyGame library.
    """

    def __init__(self, sudoku=None):
        pygame.init()
        pygame.display.set_caption("Sudoku")
        if not sudoku:
            self.sudoku = Sudoku()
            self.sudoku.generate(DIFFICULTY)
        else:
            self.sudoku = sudoku

        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))

        background = pygame.image.load("images/background.png").convert()
        self._screen.blit(background, (0, 0))

        board = pygame.image.load("images/board.png")
        self._screen.blit(board, (SUDOKUX, SUDOKUY))
        self._tiles = self._create_tiles(self.sudoku, SUDOKUX, SUDOKUY)
        self._current_tile = None
        self._draw_ui()
        self._draw()

    @staticmethod
    def _create_tiles(sudoku, initX=0, initY=0):
        """
        Create "Tile" objects collection.

        [[Tile]] is collection of tiles (cells) of current sudoku board.
        """
        def fxy(t, it):
            return 41*t + it + 2 + 4*(t//3)
        return [[Tile(sudoku(i, j), fxy(j, initX),
                      fxy(i, initY), i, j, 40)
                 for j in range(0, 9)] for i in range(0, 9)]

    def _draw_ui(self):
        """Draw Menu and Title."""
        self.menu_texts = {}
        self.menu = {}
        for size, word, x, y in [(100, "SUDOKU", WIDTH//2, 80),
                                 (10, "WG 2018", WIDTH - 30, HEIGHT - 10),
                                 (20, NEW_GAME, WIDTH//6, 180),
                                 (20, SOLVE, WIDTH//2, 180),
                                 (20, CHECK, 5*WIDTH//6, 180),
                                 (20, HINT, WIDTH//6, 220),
                                 (20, LOAD, WIDTH//2, 220),
                                 (20, SAVE, 5*WIDTH//6, 220)]:
            font = pygame.font.Font(FONT, size)
            self.menu_texts[word] = font.render(word, 1, MENU_FONT_COLOR)
            self.menu[word] = self.menu_texts[word].get_rect()
            self.menu[word].centerx = x
            self.menu[word].centery = y
            self._screen.blit(self.menu_texts[word], self.menu[word])

    def _draw(self):
        """Handle IO events and update display."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self._handle_mouse(event.pos)
                elif (event.type == pygame.KEYUP):
                    self._handle_keyboard(event.key)
            pygame.display.flip()

    def _handle_keyboard(self, key):
        """Handle keys pressed on keyboard."""
        valid_keys = {pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2,
                      pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5,
                      pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8,
                      pygame.K_9: 9, pygame.K_BACKSPACE: 0, pygame.K_DELETE: 0}
        if key in valid_keys and self._current_tile:
            i, j = self._current_tile.board_coordinates
            self._current_tile.font_color = COLORS["blue"]
            self._current_tile.value = valid_keys[key]
            self.sudoku.put(i, j, self._current_tile.value)

    def _handle_mouse(self, coordinates):
        """Handle mouse position and collisions with proper parts of UI."""
        x, y = coordinates
        for row in self._tiles:
            for tile in row:
                if tile.rectangle.collidepoint(x, y):
                    if tile.is_fillable:
                        if self._current_tile:
                            self._current_tile.toggle_highlight()
                        tile.toggle_highlight()
                        self._current_tile = tile if tile.is_highlighted else None

        menu_functions = {NEW_GAME: self.on_new_game,
                          SOLVE: self.on_solve,
                          CHECK: self.on_check,
                          HINT: self.on_give_hint,
                          SAVE: self.on_save,
                          LOAD: self.on_load}

        for action, rectangle in self.menu.items():
            if rectangle.collidepoint(x, y):
                menu_functions[action]()

    def on_new_game(self):
        """Update sudoku and board on GUI with new sudoku board."""
        self.sudoku = Sudoku()
        self.sudoku.generate(DIFFICULTY)
        self._tiles = self._create_tiles(self.sudoku, SUDOKUX, SUDOKUY)

    def on_solve(self):
        """
        Show solution to sudoku.

        Pre-filled tiles stay black.
        """
        solved, solution = solve(self.sudoku)
        if solved:
            self.sudoku = solution
            self._tiles = self._create_tiles(solution, SUDOKUX, SUDOKUY)
        self.on_check()

    def on_check(self):
        """
        Check whether current sudoku is solvable.

        If it is solvable, tiles become green. If it isn't - red.
        """
        solved, solution = solve(self.sudoku)
        if solved:
            for row in self._tiles:
                for tile in row:
                    tile.font_color = COLORS["green"]
        else:
            for row in self._tiles:
                for tile in row:
                    tile.font_color = COLORS["red"]

    def on_give_hint(self):
        """Place random tile from solution."""
        solved, solution = solve(self.sudoku)
        if solved:
            left_to_fill = [(i, j) for i in range(0, 9) for j in range(0, 9)
                            if self._tiles[i][j].value == 0]
            if left_to_fill:
                i, j = random.choice(left_to_fill)
            else:
                i, j = 0, 0
            self.sudoku.put(i,j, solution(i,j))
            self._tiles[i][j].value = solution(i, j)
            self._tiles[i][j].font_color = COLORS["green"]
        self.on_check()

    def on_load(self):
        with open("save.sudoku", mode='rb') as f:
            saved_game = pickle.load(f)
            self.sudoku = saved_game["sudoku"]
            self._tiles = self._create_tiles(self.sudoku, SUDOKUX, SUDOKUY)
            for i, j in saved_game["readonly_tiles"]:
                self._tiles[i][j].is_fillable = True
                self._tiles[i][j].font_color = COLORS["blue"]
        print("Game loaded successfully")


    def on_save(self):
        saved_game = {"sudoku": self.sudoku,
                      "readonly_tiles": [tile.board_coordinates for row in self._tiles
                                         for tile in row if tile.is_fillable]}
        with open("save.sudoku", mode='wb') as f:
            pickle.dump(saved_game, f)
        print("Game saved successfully")




class Tile:

    """Represent one tile (cell) of sudoku board."""

    def __init__(self, value, x, y, sudoku_i, sudoku_j, size):
        self.is_fillable = not bool(value)
        self.is_highlighted = False
        self._font_color = COLORS["blue"] if self.is_fillable else COLORS["black"]
        self._value = value
        self.sudoku_i, self.sudoku_j = sudoku_i, sudoku_j

        self._color_square = pygame.Surface((size, size)).convert()
        self._color_square.fill(COLORS["white"], None, pygame.BLEND_RGB_ADD)
        self._color_square_rect = self._color_square.get_rect()
        self._color_square_rect = self._color_square_rect.move(x + 1, y + 1)
        self._screen = pygame.display.get_surface()
        self.rectangle = pygame.Rect(x, y, size, size)
        self._draw()

    @property
    def board_coordinates(self):
        return self.sudoku_i, self.sudoku_j

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, color):
        if self.is_fillable:
            self._font_color = color
        self._draw()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._draw()

    def _draw(self):
        font = pygame.font.Font(FONT, 30)
        text = font.render(str(self._value) if self._value else "", 1, self.font_color)
        textpos = text.get_rect()
        textpos.centerx = self.rectangle.centerx
        textpos.centery = self.rectangle.centery
        self._screen.blit(self._color_square, self._color_square_rect)
        self._screen.blit(text, textpos)

    def toggle_highlight(self):
        self._color_square.fill(COLORS["lightblue"] if not
                                self.is_highlighted else COLORS["white"])
        self.is_highlighted = not(self.is_highlighted)
        self._draw()


if __name__ == "__main__":
        game = GUI()
        game.start()
