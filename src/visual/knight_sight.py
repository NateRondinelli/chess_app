import tkinter as tk
from tkinter import ttk
import math
import chess

LIGHT_COLOR = "#B1C1F6"
DARK_COLOR = "#608065"
FLASH_COLOR_1 = "#E8E8E8"
FLASH_COLOR_2 = "#666666"
FLASH_COLOR_3 = "#ff9b4b"
SQUARE_SIZE = 65
PADDING = 10
BOARD_WIDTH = 8 * SQUARE_SIZE + 2 * PADDING
BOARD_HEIGHT = BOARD_WIDTH
DELAY = 75
TOGGLES = 5

FILES = "abcdefgh"
RANKS = "12345678"
PIECES = [chess.Piece(piece, color) for piece in chess.PIECE_TYPES for color in chess.COLORS]


def legal_squares(square):
    _board = chess.Board(None)
    _board.set_piece_at(square, chess.Piece(chess.KNIGHT, chess.WHITE))
    return [move.to_square for move in _board.legal_moves if move.from_square == square]


def xy_from_square(square):
    _row = 7 - math.floor(square / 8)
    _col = square % 8
    _x = (_col + 0.5) * SQUARE_SIZE + PADDING
    _y = (_row + 0.5) * SQUARE_SIZE + PADDING
    return _x, _y


def square_from_xy(_x, _y):
    _x -= PADDING
    _y -= PADDING
    _col = math.floor(_x / SQUARE_SIZE)
    _row = math.floor(_y / SQUARE_SIZE)
    _col = 7 if _col > 7 else max(_col, 0)
    _row = 7 if _row > 7 else max(_row, 0)
    return (7 - _row) * 8 + _col


class KnightBoard(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(
            self,
            parent,
            borderwidth=5,
            relief="sunken",
            width=BOARD_WIDTH + 2 * PADDING,
            height=BOARD_HEIGHT + 2 * PADDING,
            padding=PADDING,
        )
        image_file_name = "images/wn.png"
        self.image = tk.PhotoImage(file=image_file_name)

        self.canvas = tk.Canvas(width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.canvas.grid(row=0, column=0)
        self.square_ids = {}
        self.create_board()
        self.toggle_on = False
        self.up = False

        self.knight_sq = 0
        self.knight = chess.Piece(chess.KNIGHT, chess.WHITE)
        self.position = chess.Board(None)
        self.position.set_piece_at(self.knight_sq, self.knight)
        _x, _y = xy_from_square(self.knight_sq)
        self.image_id = self.canvas.create_image(_x, _y, image=self.image)
        self.start()

    def create_board(self):
        for row in range(0, 8):
            y1 = row * SQUARE_SIZE + PADDING
            y2 = y1 + SQUARE_SIZE
            for col in range(0, 8):
                x1 = col * SQUARE_SIZE + PADDING
                x2 = x1 + SQUARE_SIZE
                square = col + 8 * (7 - row)
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                rect_id = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=DARK_COLOR,
                )
                self.square_ids[square] = rect_id

    def update_position(self):
        _row = math.floor(self.knight_sq / 8)
        _col = self.knight_sq % 8
        if self.knight_sq == 0 or self.knight_sq == 56:
            self.up = not self.up
        if _row % 2 == 0:
            _switch = 7 if self.up else 0
            _increment = 1 if self.up else -1
        else:
            _increment = -1 if self.up else 1
            _switch = 0 if self.up else 7
        if _col == _switch:
            self.knight_sq += 8 if self.up else -8
        else:
            _col += _increment
            self.knight_sq = _row * 8 + _col
        self.position = chess.Board(None)
        self.position.set_piece_at(self.knight_sq, self.knight)
        sq_x, sq_y = xy_from_square(self.knight_sq)
        self.canvas.coords(self.image_id, sq_x, sq_y)

    def shimmer(self, count):
        self.flash_toggle()
        if count > 0:
            root.after(DELAY, self.shimmer, count - 1)
        else:
            self.update_position()
            self.start()

    def toggle_square(self, sq_id, color, flash):
        if self.toggle_on:
            self.canvas.itemconfig(sq_id, fill=color)
        else:
            self.canvas.itemconfig(sq_id, fill=flash)

    def flash_toggle(self):
        _row = 7 - math.floor(self.knight_sq / 8)
        _col = self.knight_sq % 8
        _squares = legal_squares(self.knight_sq)
        for _square in _squares:
            _color = LIGHT_COLOR if (_row + _col) % 2 == 1 else DARK_COLOR
            _flash = FLASH_COLOR_1 if _color == DARK_COLOR else FLASH_COLOR_2
            sq_id = self.square_ids[_square]
            self.toggle_square(sq_id, _color, _flash)
            second_moves = legal_squares(_square) 
            for second_square in second_moves:
                _color = LIGHT_COLOR if (_row + _col) % 2 != 1 else DARK_COLOR
                _flash = FLASH_COLOR_1 if _color != DARK_COLOR else FLASH_COLOR_3
                second_sq_id = self.square_ids[second_square]
                self.toggle_square(second_sq_id, _color, _flash)
        self.toggle_on = not self.toggle_on

    def start(self):
        self.shimmer(TOGGLES)


if __name__ == "__main__":
    root = tk.Tk()
    outer_frame = ttk.Frame(root, padding=40)
    board = KnightBoard(outer_frame)
    board.grid(row=0, column=0)
    outer_frame.grid(row=0, column=0)
    root.mainloop()
