from checkers_logic import *


def initial_board_for_converting_to_king():
    ret = []

    for i in range(8):
        ith_row = []
        ret.append(ith_row)

        for j in range(8):
            ret[i].append(None)

    ret[1][7] = Piece(0)
    ret[0][0] = Piece(1)

    return ret


def initial_board_for_jump_detection():
    ret = []

    for i in range(8):
        ith_row = []
        ret.append(ith_row)

        for j in range(8):
            ret[i].append(None)

    ret[1][3] = Piece(0)
    ret[2][4] = Piece(1)

    return ret


def initial_board_for_no_opponent_piece_detection():
    ret = []

    for i in range(8):
        ith_row = []
        ret.append(ith_row)

        for j in range(8):
            ret[i].append(None)

    ret[6][0] = Piece(0)

    return ret


board = initial_board()

white_piece = Piece(0, False)
black_piece = Piece(1, False)
white_piece_king = Piece(0, True)
black_piece_king = Piece(1, True)


def test_surroundings():
    assert surroundings(white_piece, 5, 2) == [(6, 3), (4, 3)]
    assert surroundings(black_piece, 5, 2) == [(4, 1), (6, 1)]
    assert surroundings(white_piece_king, 5, 2) == [(4, 1), (6, 3), (6, 1), (4, 3)]
    assert surroundings(black_piece_king, 5, 2) == [(4, 1), (6, 3), (6, 1), (4, 3)]

    assert surroundings(white_piece, 9, 5) == []
    assert surroundings(black_piece, 9, 5) == []
    assert surroundings(white_piece_king, 9, 5) == []
    assert surroundings(black_piece_king, 9, 2) == []


def test_possible_jumps():
    assert possible_jumps(white_piece, 2, 4, board) == [(4, 6), (0, 6)]
    assert possible_jumps(black_piece, 1, 3, board) == [(3, 1)]


def test_move_positions():
    assert move_positions(white_piece, 6, 1, board) == [(7, 2), (5, 2)]
    assert move_positions(white_piece, 0, 2, board) == [(1, 3)]
    assert move_positions(black_piece, 1, 5, board) == [(0, 4), (2, 4)]
    assert move_positions(black_piece, 5, 5, board) == [(4, 4), (6, 4)]

    assert move_positions(white_piece, 0, 0, board) == []
    assert move_positions(white_piece, 4, 0, board) == []
    assert move_positions(black_piece, 1, 7, board) == []
    assert move_positions(black_piece, 3, 7, board) == []


def test_convert_to_king():
    board1 = initial_board_for_converting_to_king()
    assert board1[1][7].king is False
    assert board1[0][0].king is False
    convert_to_king(board1)
    assert board1[1][7].king is True
    assert board1[0][0].king is True


def test_jump_detection():
    board1 = initial_board_for_jump_detection()
    assert jump_detection(board1, 0) == [(1, 3)]
    assert jump_detection(board1, 1) == [(2, 4)]


def test_no_opponent_piece_detection():
    board1 = initial_board_for_jump_detection()
    assert no_opponent_piece_detection(board1, 0) is False
    assert no_opponent_piece_detection(board1, 1) is False

    board2 = initial_board_for_no_opponent_piece_detection()
    assert no_opponent_piece_detection(board2, 0) is True
    assert no_opponent_piece_detection(board2, 1) is False
