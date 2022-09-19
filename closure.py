import chess
board = chess.Board(fen='r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1 b - - 0 1')
print(board.piece_map())

def x_closure(pos, board: chess.Board):
    piece = board.piece_at(pos)
    xc = []
    empty_board = chess.BaseBoard.empty()
    empty_board.set_piece_at(pos, piece)
    for attack in empty_board.attacks(pos):
        opiece = board.piece_at(attack)
        if opiece:
            if opiece.color != piece.color:
                xc.append((attack, opiece))
    return xc

def d_closure(pos, board: chess.Board):
    piece = board.piece_at(pos)
    ac = []
    for attack in board.attacks(pos):
        opiece = board.piece_at(attack)
        if opiece:
            if opiece.color == piece.color:
                ac.append((attack, opiece))
    return ac

def a_closure(pos, board: chess.Board):
    piece = board.piece_at(pos)
    ac = []
    for attack in board.attacks(pos):
        opiece = board.piece_at(attack)
        if opiece:
            if opiece.color != piece.color:
                ac.append((attack, opiece))
    return ac


def r_closure(pos, board):
    rc = {}
    for move in board.attacks(pos):
        opiece = board.piece_at(move)
        if not opiece:
            rc[move] = 1-(7*chess.square_distance(pos, move))/64
    return rc

rc_map = {}
ac_map = {}
dc_map = {}
xc_map = {}
for pos, piece in board.piece_map().items():
    rc_map[(piece, pos)] = r_closure(pos, board)
    ac_map[(piece, pos)] = a_closure(pos, board)
    dc_map[(piece, pos)] = d_closure(pos, board)
    xc_map[(piece, pos)] = x_closure(pos, board)

print(xc_map)
print(rc_map)
# Ask Steve to convert to BinaryVector like representation for a/d/x closure
piece_symbols = 'PNBRQK'
piece_symbols += piece_symbols.lower()
all_pieces = [chess.Piece.from_symbol(symbol) for symbol in piece_symbols]
# 32x4x64
# Keep in mind promotions for pawns. 
def rc_to_vector(rc_map):
    for piece in all_pieces:
        # Ask Steve for piece to position map.