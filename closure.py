from multiprocessing.sharedctypes import Value
import numpy as np
import chess
from chess import Piece
# position = chess.Board(fen='r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1 b - - 0 1')
# position = chess.Board(fen='8/8/8/7b/8/8/8/7R w - - 0 1')
position = chess.Board(fen='2rq1rk1/1p1n1pb1/p2pp1pp/7P/4PP2/1NN2QP1/PPP5/2KRR3 w - - 0 1')

print(position.piece_map())

BOARD_SIZE=8
ALL_PIECE_SYMBOLS = 'rnbqkbnrpppppppp'

def x_closure(square, position: chess.Board):
    '''X-ray attack closure'''
    piece = position.piece_at(square)
    xc = []
    empty_board = chess.BaseBoard.empty()
    empty_board.set_piece_at(square, piece)
    for attack in empty_board.attacks(square):
        opiece = position.piece_at(attack)
        if opiece:
            if opiece.color != piece.color:
                xc.append((attack, opiece))
    return xc

def d_closure(square, position: chess.Board):
    '''Defence closure'''
    piece = position.piece_at(square)
    ac = []
    for attack in position.attacks(square):
        opiece = position.piece_at(attack)
        if opiece:
            if opiece.color == piece.color:
                ac.append((attack, opiece))
    return ac

def a_closure(square, position: chess.Board):
    '''Attack closure'''
    piece = position.piece_at(square)
    ac = []
    for attack in position.attacks(square):
        opiece = position.piece_at(attack)
        if opiece:
            if opiece.color != piece.color:
                ac.append((attack, opiece))
    return ac


def r_closure(square, position):
    '''Reachable squares closure
    Ganguly et al. says that capture squares are not included in reachability closure. '''
    rc = [0]*64
    for move in position.attacks(square):
        other_piece = position.piece_at(move)
        if not other_piece:
            rc[move] = 1-(7*chess.square_distance(square, move))/64
    return rc


piece_values = dict(zip('pnbrqk', [.1, .3, .3, .5, .9, 1]))

def get_all_pieces():
    all_pieces = list(ALL_PIECE_SYMBOLS+ALL_PIECE_SYMBOLS.upper())
    return all_pieces

def build_piece_index(piece_map):
    """
    It takes a chess position and returns a dictionary that maps each piece to a unique integer
    
    :param position: The chess board position
    :type position: chess.Board
    :return: A dictionary with keys as tuples of (piece, square) and values as index.
    """
    all_pieces = get_all_pieces()
    piece_index = {}
    for square, piece in piece_map.items():
        try:
            index = all_pieces.index(piece.symbol())
        except ValueError as e:
            try:
                index = all_pieces.index(Piece(chess.PAWN, piece.color))
            except ValueError as ee:
                raise ValueError('Ab lag gaya!')
        all_pieces.pop(index)
        piece_index[(piece, square)] = index
    return piece_index

def closure_to_vector(closure_map, piece_index):
    closure_tensor = [[0]*(BOARD_SIZE**2) for _ in get_all_pieces()]
    for key in closure_map: 
        for items in closure_map[key]:
            closure_tensor[piece_index[key]][items[0]]=piece_values[items[1].symbol().lower()]
    return closure_tensor

def r_closure_to_vector(closure_map, piece_index):
    closure_tensor = [[0]*(BOARD_SIZE**2) for _ in get_all_pieces()]
    for key in closure_map: 
        closure_tensor[piece_index[key]]=closure_map[key]
    return closure_tensor

def build_closure_tensor(position):
    rc_map = {}
    ac_map = {}
    dc_map = {}
    xc_map = {}
    piece_index = build_piece_index(position.piece_map())
    for square, piece in position.piece_map().items():
        rc_map[(piece, square)] = r_closure(square, position)
        ac_map[(piece, square)] = a_closure(square, position)
        dc_map[(piece, square)] = d_closure(square, position)
        xc_map[(piece, square)] = x_closure(square, position)

    closure_tensor = []
    # for closure in [ac_map, dc_map, xc_map]:
    #     closure_tensor.append(closure_to_vector(closure, piece_index))
    closure_tensor.append(r_closure_to_vector(rc_map, piece_index))
    return closure_tensor

# 4x32x64
# Keep in mind promotions for pawns. 

closure_tensor = build_closure_tensor(position)

print(np.sum(np.array(closure_tensor)))