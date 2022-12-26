import tkinter as tk
from tkinter import ttk
import math
import chess
import random

LIGHT_COLOR = "#81A1D6"
DARK_COLOR = "#608065"
SQUARE_SIZE = 65
PADDING = 10
BOARD_WIDTH = 8 * SQUARE_SIZE + 2 * PADDING
BOARD_HEIGHT = BOARD_WIDTH
RANKS = "12345678"
FILES = "abcdefgh"
SQUARE_NAMES = [chess.square_name(s) for s in range(0, 64)]


def get_ready_msg():
    return "Press button to Play"


def on_same_diagonal(_sq1, _sq2):
    board = chess.Board(fen=None)
    board.set_piece_at(_sq1, chess.Piece(chess.BISHOP, chess.WHITE))
    return True if _sq2 in board.attacks(_sq1) else False


def too_close(_sq1, _sq2):
    file_diff = abs(chess.square_file(_sq1) - chess.square_file(_sq2))
    rank_diff = abs(chess.square_rank(_sq1) - chess.square_rank(_sq2))
    return file_diff < 3 and rank_diff < 3


def diag_play():
    def get_diagplay_squares():
        square_a = random.randint(0, 63)
        color_a = square_color(square_a)
        square_b = random.randint(0, 63)
        color_b = square_color(square_b)
        while square_b == square_a or (color_a != color_b) \
                or on_same_diagonal(square_a, square_b)\
                or too_close(square_a, square_b):
            square_b = random.randint(0, 63)
            color_b = square_color(square_b)
        return square_a, square_b

    def get_play_msg():
        s1 = "Where do diagonals intersect?\n"
        s2 = "Enter square(s) in common. "
        return s1 + s2

    def get_eval_msg(_sq1, _sq2, entered):
        s1 = f"Bishops on {chess.square_name(_sq1)} and {chess.square_name(_sq2)}.\n"
        s2 = f"You entered {', '.join(entered)}\n"
        return s1 + s2

    def reset_play():
        message_pane.config(text=get_ready_msg())
        square_label.config(text="")
        play_button.config(text="Play", command=diag_play)
        entry.unbind("<Return>")
        play_button.focus()
        play_button.bind("<Return>", lambda e: diag_play())
        hide_board()
        show_board()

    def process_input():
        entered = entry.get().split(",")
        entered = [e.strip() for e in entered]
        if any(e not in SQUARE_NAMES for e in entered):
            bishop_text = square_label.cget("text")
            if "Please enter" in bishop_text:
                pass
            else:
                square_label.config(text=f"Please enter valid algebraic square names: {bishop_text}")
            entry.delete(0, tk.END)
        else:
            message_pane.config(text=get_eval_msg(sq1, sq2, entered))
            show_board()
            for _sq in (sq1, sq2):
                canvas.itemconfig(circle_ids[_sq], state="normal")
            for _sq in correct:
                toggle_square_color(_sq)
            is_correct = True
            for e in entered:
                if e == "1":
                    if correct != {-1}:
                        is_correct = False
                    break
                sq = chess.parse_square(e)
                if sq not in correct:
                    is_correct = False
                else:
                    correct.remove(sq)
            if len(correct) > 0:
                is_correct = False
            if is_correct:
                square_label.config(text="Correct!")
            else:
                square_label.config(text="Incorrect")
            entry.delete(0, tk.END)
            entry.config(state="disabled")
            entry.bind("<Return>", lambda e: reset_play())
            play_button.config(text="Reset", command=reset_play)

    hide_board()
    (sq1, sq2) = get_diagplay_squares()
    message_pane.config(text=get_play_msg())
    square_label.config(text=f"Bishops on {chess.square_name(sq1)} and {chess.square_name(sq2)}")
    entry.config(state="normal")
    entry.bind("<Return>", lambda e: process_input())
    play_button.config(text="Enter", command=process_input)
    entry.focus()

    board1 = chess.Board('8/8/8/8/8/8/8/8 w - - 0 1')
    board2 = chess.Board('8/8/8/8/8/8/8/8 w - - 0 1')
    board1.set_piece_at(sq1, chess.Piece(chess.BISHOP, chess.WHITE))
    board2.set_piece_at(sq2, chess.Piece(chess.BISHOP, chess.WHITE))
    sq1_squares = set(board1.attacks(sq1))
    sq2_squares = set(board2.attacks(sq2))
    correct = sq1_squares.intersection(sq2_squares)


def hide_board():
    for square_id in range(0, 64):
        # print(square_id)
        canvas.itemconfig(square_ids[square_id], state="hidden")
        canvas.itemconfig(circle_ids[square_id], state="hidden")
        canvas.itemconfig(text_ids[square_id], state="hidden")


def show_board():
    for square_id in range(0, 64):
        canvas.itemconfig(square_ids[square_id], state="normal", fill=square_color(square_id))
        canvas.itemconfig(circle_ids[square_id], state="hidden")
        canvas.itemconfig(text_ids[square_id], state="normal")


def square_from_coords(x, y):
    file = math.floor((x - PADDING)/SQUARE_SIZE)
    rank = 7 - math.floor((y - PADDING)/SQUARE_SIZE)
    return file + 8 * rank


def square_from_rc(row_num, col_num):
    return col_num + 8 * (7 - row_num)


def square_color(sq):
    row_num = math.floor(sq/8)
    col_num = sq % 8
    return "black" if (row_num + col_num) % 2 == 0 else "white"


def toggle_square_color(sq):
    _rect = square_ids[sq]
    state = canvas.itemcget(_rect, "fill")
    if state in {"white", "black"}:
        canvas.itemconfig(_rect, fill="red")
    else:
        canvas.itemconfig(_rect, fill=square_color(sq))


def get_oval_bounds(a, b):
    ratio_1 = 0.28
    ratio_2 = 0.72
    _x1 = int(math.floor(ratio_1 * SQUARE_SIZE + a))
    _x2 = int(math.floor(ratio_2 * SQUARE_SIZE + a))
    _y1 = int(math.floor(ratio_1 * SQUARE_SIZE + b))
    _y2 = int(math.floor(ratio_2 * SQUARE_SIZE + b))

    return _x1, _y1, _x2, _y2


def process_left_click(event):
    # print(event.x, event.y)
    sq = square_from_coords(event.x, event.y)
    # print(chess.square_name(sq))
    toggle_square_color(sq)


root = tk.Tk()
root.minsize(width=BOARD_WIDTH, height=BOARD_HEIGHT)
frame = ttk.Frame(root)
frame.grid(row=0, column=0)
canvas = tk.Canvas(frame, width=BOARD_WIDTH, height=BOARD_HEIGHT, highlightthickness=0, borderwidth=0)

square_ids = {}
circle_ids = {}
text_ids = {}
color = "black"
for row in range(0, 8):
    y1 = row * SQUARE_SIZE + PADDING
    y2 = y1 + SQUARE_SIZE
    for col in range(0, 8):
        x1 = col * SQUARE_SIZE + PADDING
        x2 = x1 + SQUARE_SIZE
        square = square_from_rc(row, col)
        # print(square)
        color = square_color(square)
        rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags=square)
        square_ids[square] = rect_id
        x3 = int(math.floor((x1 + x2) / 2))
        y3 = int(math.floor((y1 + y2) / 2))
        square_name = chess.square_name(square)
        text_id = canvas.create_text(x3, y3, text=square_name, fill=color)
        text_ids[square] = text_id
        (x4, y4, x5, y5) = get_oval_bounds(x1, y1)
        circle_color = "black" if color == "white" else "white"
        circle_id = canvas.create_oval(x4, y4, x5, y5, fill=circle_color, state="hidden")
        circle_ids[square] = circle_id
        canvas.lift(text_id)

canvas.bind('<ButtonPress-1>', process_left_click)
canvas.grid(row=0, column=0, columnspan=3)

message_pane = ttk.Label(frame, text=get_ready_msg())
message_pane.grid(row=1, column=0, rowspan=2, sticky="w")

square_label = ttk.Label(frame, text="")
square_label.grid(row=1, column=1, sticky="n")

entry = ttk.Entry(frame, width=15, state="disabled")
entry.grid(row=2, column=1, sticky="we")

play_button = ttk.Button(frame, text="Play", width=10, command=diag_play)
play_button.grid(row=1, column=2, sticky="e")
play_button.focus()
play_button.bind("<Return>", lambda e: diag_play())

root.mainloop()
