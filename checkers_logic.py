def bounds_check(f):
    def ret_func(*args):
        x_lst = f(*args)

        y = []
        for x in x_lst:
            x1, x2 = x
            if 8 > x1 >= 0 and x2 < 8 and x2 >= 0:
                y.append(x)

        return y

    return ret_func


@bounds_check
def surroundings(piece, x, y):
    ret = []
    if piece.king:
        ret.append((x - 1, y - 1))
        ret.append((x + 1, y + 1))
        ret.append((x + 1, y - 1))
        ret.append((x - 1, y + 1))
        return ret

    else:
        if piece.color == 0:
            ret.append((x + 1, y + 1))
            ret.append((x - 1, y + 1))
            return ret
        else:
            ret.append((x - 1, y - 1))
            ret.append((x + 1, y - 1))
            return ret


@bounds_check
def possible_jumps(piece, x, y, board):
    positions = surroundings(piece, x, y)

    ret = []

    for p in positions:
        i, j = p
        if board[i][j] is not None:
            if board[i][j].color != piece.color:
                ret.append((x + 2 * (i - x), y + 2 * (j - y)))

    return ret


def jump_positions(piece, x, y, board):
    positions = possible_jumps(piece, x, y, board)

    ret = []

    for p in positions:
        i, j = p

        if board[i][j] is None:
            ret.append((i, j))

    return ret


def move_positions(piece, x, y, board):
    positions = surroundings(piece, x, y)

    ret = []
    for p in positions:
        i, j = p

        if board[i][j] is None:
            ret.append((i, j))

    return ret


def initial_board():
    ret = []

    for i in range(8):
        ith_row = []
        ret.append(ith_row)

        for j in range(8):
            ret[i].append(None)

    for i in range(0, 4, 2):
        for j in range(0, 7, 2):
            ret[j][i] = Piece(0)
            ret[1 + j][7 - i] = Piece(1)

    for j in range(0, 7, 2):
        ret[1 + j][1] = Piece(0)
        ret[j][6] = Piece(1)

    return ret


def convert_to_king(board):
    for j in range(8):
        if board[j][0] is not None:
            if board[j][0].color == 1 and board[j][0].king is False:
                board[j][0].king = True

        if board[j][7] is not None:
            if board[j][7].color == 0 and board[j][7].king is False:
                board[j][7].king = True

    return


def no_move_detection(board, turn):
    ret = True

    for x in range(8):
        for y in range(8):
            if board[x][y] is not None and board[x][y].color == turn:
                mvLst = move_positions(board[x][y], x, y, board)
                jmpLst = jump_positions(board[x][y], x, y, board)

                if len(mvLst) == 0 and len(jmpLst) == 0:
                    pass
                else:
                    ret = False
    return ret


def no_opponent_piece_detection(board, turn):
    ret = True

    if turn == 0:
        opponent = 1
    else:
        opponent = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] is not None and board[x][y].color == opponent:
                ret = False

    return ret


def jump_detection(board, turn):
    ret = []

    for x in range(8):
        for y in range(8):
            if board[x][y] is not None and board[x][y].color == turn:
                jmpLst = jump_positions(board[x][y], x, y, board)

                if len(jmpLst) == 0:
                    pass
                else:
                    ret.append((x, y))
    return ret


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king

    def __eq__(self, other):
        if isinstance(other, Piece):
            return (self.color == other.color) and (self.king == other.king)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.color, self.king))
