import tkinter as tk
from tkinter import ttk
import math
import chess

LIGHT_COLOR = "#B1C1F6"
DARK_COLOR = "#608065"
SQUARE_SIZE = 65
PADDING = 10
BOARD_WIDTH = 8 * SQUARE_SIZE + 2 * PADDING
BOARD_HEIGHT = BOARD_WIDTH

FILES = "abcdefgh"
RANKS = "12345678"
PIECES = [chess.Piece(piece, color) for piece in chess.PIECE_TYPES for color in chess.COLORS]


def legal_squares(square_name, _board):
    return [chess.square_name(move.to_square)
            for move in _board.legal_moves
            if chess.square_name(move.from_square) == square_name]


def xy_from_square_name(square_name):
    _row = 7 - RANKS.index(square_name[1])
    _col = FILES.index(square_name[0])
    _x = (_col + 0.5) * SQUARE_SIZE + PADDING
    _y = (_row + 0.5) * SQUARE_SIZE + PADDING
    return _x, _y


def square_name_from_xy(_x, _y):
    _x -= PADDING
    _y -= PADDING
    _col = math.floor(_x / SQUARE_SIZE)
    _row = math.floor(_y / SQUARE_SIZE)
    _col = 7 if _col > 7 else max(_col, 0)
    _row = 7 if _row > 7 else max(_row, 0)
    _file = FILES[_col]
    _rank = RANKS[7 - _row]
    return _file + _rank


class BoardGui(ttk.Frame):
    def __init__(self, parent, _fen=None):
        ttk.Frame.__init__(
            self,
            parent,
            borderwidth=5,
            relief="sunken",
            width=BOARD_WIDTH + 2 * PADDING,
            height=BOARD_HEIGHT + 2 * PADDING,
            padding=PADDING,
        )
        self.images = {}
        for piece in PIECES:
            image_file_name = "images/"
            image_file_name += "w" if piece.color else "b"
            image_file_name += piece.symbol().lower() + ".png"
            self.images[piece] = tk.PhotoImage(file=image_file_name)

        # create a canvas
        self.canvas = tk.Canvas(width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.canvas.grid(row=0, column=0)
        # self.frame = tk.Frame(self)
        # self.frame.grid(row=0, column=1)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None, "square": "", "legal": []}

        # self.bb_image = tk.PhotoImage(file="images/bb.png")
        # self.wb_image = tk.PhotoImage(file="images/wb.png")

        self.square_ids = {}
        self.create_board()
        if _fen == "":
            self.position = chess.Board()
        else:
            self.position = chess.Board(_fen)

        # wb_x, wb_y = xy_from_square_name("e2")
        # bb_x, bb_y = xy_from_square_name("f7")
        #
        # self.create_token(wb_x, wb_y, "white")
        # self.create_token(bb_x, bb_y, "black")
        for square, piece in self.position.piece_map().items():
            _x, _y = xy_from_square_name(chess.square_name(square))
            self.create_token(_x, _y, piece)

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)

    def create_board(self):
        for row in range(0, 8):
            y1 = row * SQUARE_SIZE + PADDING
            y2 = y1 + SQUARE_SIZE
            for col in range(0, 8):
                x1 = col * SQUARE_SIZE + PADDING
                x2 = x1 + SQUARE_SIZE
                square = col + 8 * (7 - row)
                # print(square)
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                rect_id = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=DARK_COLOR,
                    tags=square,
                )
                # # Test calculations for correct location of square centers by placing small dots
                # dot_x, dot_y = xy_from_square_name(chess.square_name(square))
                # print(f"{chess.square_name(square)}: {dot_x}, {dot_y}")
                # print(f"Output from function: {xy_from_square_name(chess.square_name(square))}")
                # self.canvas.create_rectangle(
                #     dot_x - 3,
                #     dot_y - 3,
                #     dot_x + 3,
                #     dot_y + 3,
                #     fill="white",
                # )
                self.square_ids[square] = rect_id

    def create_token(self, x, y, piece):
        """Create a token at the given coordinate in the given color"""
        _image = self.images[piece]
        _sq = square_name_from_xy(x, y)
        self.canvas.create_image(x, y, image=_image, tags=["token", _sq])

    def drag_start(self, event):
        """Beginning drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.canvas.tag_raise(self._drag_data["item"])
        self._drag_data["x"] = _x = event.x
        self._drag_data["y"] = _y = event.y
        self._drag_data["start"] = _sq = square_name_from_xy(_x, _y)
        # print(f"Start: {square_name_from_xy(_x, _y)}")
        self._drag_data["legal"] = legal_squares(_sq, self.position)
        print(f"Start: {_sq}, Legal moves: {str(self._drag_data['legal'])}")

    def drag_stop(self, event):
        """End drag of an object"""
        # snap position of image to square center
        _x, _y = event.x, event.y
        _sq = square_name_from_xy(_x, _y)
        if _sq in self._drag_data["legal"]:
            print(f"Moved to {_sq}")
            # .moveto() sets upper left corner to x, y; .coords() sets center to x, y
            sq_x, sq_y = xy_from_square_name(_sq)
            move = chess.Move.from_uci(self._drag_data["start"] + _sq)
            if chess.parse_square(_sq) in self.position.piece_map().keys():
                self.canvas.delete(_sq)
            self.canvas.itemconfig(self._drag_data["start"], tags=["token", _sq])
            self.position.push(move)
            print(self.position)
        else:
            sq_x, sq_y = xy_from_square_name(self._drag_data["start"])
            # print(f"Recover to square: {self._drag_data['start']}")
        self.canvas.coords(self._drag_data["item"], sq_x, sq_y)
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["start"] = ""
        self._drag_data["legal"] = []
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # # compute how much the mouse has moved
        # delta_x = event.x - self._drag_data["x"]
        # delta_y = event.y - self._drag_data["y"]
        # # move the object the appropriate amount
        # self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # print(f"{event.x}, {event.y}")
        if 2 * PADDING < event.x < BOARD_WIDTH - PADDING and 2 * PADDING < event.y < BOARD_HEIGHT - PADDING:
            self.canvas.coords(self._drag_data["item"], event.x, event.y)
            # record the new position
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            # print(square_name_from_xy(event.x, event.y))


if __name__ == "__main__":
    root = tk.Tk()
    outer_frame = ttk.Frame(root, padding=40)
    # fen = "8/4B3/8/5N2/8/2k5/8/K7 w - - 0 1"  # KBNvK TB 15 Beginning
    # fen = "8/8/8/4B3/8/4K3/5N2/5k2 w - - 0 1"  # KBNvK TB 15 Late
    fen = ""
    board = BoardGui(outer_frame, fen)
    board.grid(row=0, column=0)
    # side_pane = ttk.Frame(root, padding=20)
    # side_pane.grid(row=0, column=1)
    # button = ttk.Button(side_pane, text="What?")
    # button.grid(row=0, column=0)
    outer_frame.grid(row=0, column=0)
    root.mainloop()
