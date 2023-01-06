import tkinter as tk
import math
import chess

SQUARE_SIZE = 50
PADDING = 10
BOARD_WIDTH = 8 * SQUARE_SIZE + 2 * PADDING
BOARD_HEIGHT = BOARD_WIDTH
RANKS = "12345678"
FILES = "abcdefgh"


def diag_play(sq1, sq2):
    sq1 = FILES.index(sq1[0]) + 8 * RANKS.index(sq1[1])
    sq2 = FILES.index(sq2[0]) + 8 * RANKS.index(sq2[1])

    board1 = chess.Board('8/8/8/8/8/8/8/8 w - - 0 1')
    board2 = chess.Board('8/8/8/8/8/8/8/8 w - - 0 1')

    board1.set_piece_at(sq1, chess.Piece(chess.BISHOP, chess.WHITE))
    board2.set_piece_at(sq2, chess.Piece(chess.BISHOP, chess.WHITE))

    sq1_squares = {chess.square_name(square) for square in board1.attacks(sq1)}
    sq2_squares = {chess.square_name(square) for square in board2.attacks(sq2)}
    correct = sq1_squares.intersection(sq2_squares)
    if len(correct) == 0:
        return {'0'}
    elif chess.square_name(sq2) in sq1_squares:
        return {'1'}
    else:
        return correct


def hide_board():
    for rect in square_ids:
        canvas.itemconfig(square_ids[rect], state="hidden")


def show_board():
    for rect in square_ids:
        canvas.itemconfig(square_ids[rect], state="normal")


def square_from_coords(x, y):
    file = FILES[math.floor((x - PADDING)/SQUARE_SIZE)]
    rank = RANKS[7 - math.floor((y - PADDING)/SQUARE_SIZE)]
    return f"{file}{rank}"


def square_from_rc(row_num, col_num):
    file = FILES[col_num]
    rank = RANKS[7 - row_num]
    return f"{file}{rank}"


def square_color(sq):
    row_num = 8 - RANKS.index(sq[1])
    col_num = FILES.index(sq[0])
    return "white" if (row_num + col_num) % 2 == 0 else "black"


def toggle_square_color(sq):
    state = canvas.itemcget(sq, "fill")
    if state in {"white", "black"}:
        canvas.itemconfig(sq, fill="red")
    else:
        canvas.itemconfig(sq, fill=square_color(sq))


def process_left_click(event):
    global clicked
    sq = square_from_coords(event.x, event.y)
    toggle_square_color(sq)
    if len(clicked) == 2:
        hide_board()
        sq1 = clicked[0]
        sq2 = clicked[1]
        correct = diag_play(sq1, sq2)

        s1 = f"Consider the diagonals from squares {sq1} and {sq2}."
        s2 = "At which points do the diagonals intersect?"
        s3 = "Enter 0 if the squares are not the same color, 1 if they lie on the same diagonal."
        s4 = "Otherwise, enter the square(s) they have in common (separated by commas): "
        print(s1)
        print(s2)
        print(s3)
        answer = input(s4)
        print(f"Correct: {correct}")
        print(f"Answer: {answer}")

        # show_board()
        clicked = []
    else:
        clicked.append(sq)


root = tk.Tk()
root.minsize(width=BOARD_WIDTH, height=BOARD_HEIGHT)
frame = tk.Frame(root)
frame.config(padx=PADDING, pady=PADDING, bg="white")
frame.grid(row=0, column=0)
canvas = tk.Canvas(frame, width=BOARD_WIDTH, height=BOARD_HEIGHT, highlightthickness=0, borderwidth=0)

color = "black"
square_ids = {}
for row in range(0, 8):
    y1 = row * SQUARE_SIZE + PADDING
    y2 = y1 + SQUARE_SIZE
    for col in range(0, 8):
        x1 = col * SQUARE_SIZE + PADDING
        x2 = x1 + SQUARE_SIZE
        square = square_from_rc(row, col)
        color = square_color(square)
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags=square)
        square_ids[square] = rect

clicked = []
canvas.bind('<ButtonPress-1>', process_left_click)
canvas.grid(row=0, column=0)

text_pane = tk.Text(frame, width=25, height=20)
text_pane.grid(row=0, column=1, sticky="ns")

root.mainloop()
