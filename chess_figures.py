WHITE = 1
BLACK = 2


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


class Board:
    def __init__(self):
        self.color = WHITE
        self.previous_move_for_pass, self.pass_figure = False, (None, None)
        self.field = [[None] * 8 for i in range(8)]
        self.field[0] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]
        self.field[1] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[6] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[7] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]

    def get_piece(self, row, col):
        return self.field[row][col]

    def can_castling0(self, row, col):
        start_ind = 0 if self.color == BLACK else 7
        if start_ind != row or col != 2:
            return False
        if (
            type(self.field[start_ind][0]) is Rook and
            type(self.field[start_ind][4]) is King
            and all(self.field[start_ind][i] is None for i in range(1, 4))
            and self.field[start_ind][0].flag_for_cast
            and self.field[start_ind][4].flag_for_cast
           ):
            return True
        return False

    def castling0(self):
        start_ind = 0 if self.color == BLACK else 7
        if self.can_castling0(start_ind, 2):
            self.color = opponent(self.color)
            self.field[start_ind][3] = self.field[start_ind][0]
            self.field[start_ind][0] = None
            # self.field[start_ind][0], self.field[start_ind][3] = None, self.field[start_ind][0] # noqa
            self.field[start_ind][2] = self.field[start_ind][4]
            self.field[start_ind][4] = None
            # self.field[start_ind][4], self.field[start_ind][2] = None, self.field[start_ind][4] # noqa
            return True
        return False

    def can_castling7(self, row, col):
        start_ind = 0 if self.color == BLACK else 7
        if start_ind != row or col != 6:
            return False
        if (
            type(self.field[start_ind][-1]) is Rook and
            type(self.field[start_ind][4]) is King
            and all(self.field[start_ind][i] is None for i in range(5, 7))
            and self.field[start_ind][-1].flag_for_cast
            and self.field[start_ind][4].flag_for_cast
        ):
            return True
        return False

    def castling7(self):
        start_ind = 0 if self.color == BLACK else 7
        if self.can_castling7(start_ind, 6):
            self.color = opponent(self.color)
            self.field[start_ind][-3] = self.field[start_ind][-1]
            self.field[start_ind][-1] = None
            # self.field[start_ind][-1], self.field[start_ind][-3] = None, self.field[start_ind][-1] # noqa
            self.field[start_ind][-2] = self.field[start_ind][4]
            self.field[start_ind][4] = self.field[start_ind][-2]
            # self.field[start_ind][4], self.field[start_ind][-2] = None, self.field[start_ind][4] # noqa
            return True
        return False

    def taking_on_the_pass(self, row, col):
        if (
            type(self.field[row][col]) is Pawn and
            self.field[row][col].flag_for_pass
        ):
            self.previous_move_for_pass, self.pass_figure = True, (row, col)
            return True
        return False

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is not None:
            return piece.char()

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if (
            type(self.field[row][col]) is Pawn and
                self.field[row][col].can_taking_pass
                (self, row, col, row1, col1)
        ):
            self.field[self.pass_figure[0]][self.pass_figure[1]] = None
            self.previous_move_for_pass = False
        elif self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1] is not None:
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        self.field[row][col] = None
        self.field[row1][col1] = piece
        if not self.taking_on_the_pass(row1, col1):
            self.previous_move_for_pass = False
        if type(piece) is King or type(piece) is Rook:
            piece.flag_for_cast = False
        self.color = opponent(self.color)
        return True


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return '\u265E'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        if (
            board.field[row1][col1] is not None and
            board.field[row1][col1].get_color()
                == board.field[row][col].get_color()
        ):
            return False
        if (
            abs(col - col1) == 1 and
            abs(row - row1) == 2) or (
                abs(col - col1) == 2
                and abs(row - row1) == 1
                                   ):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __repr__(self):
        return f"Knight({self.color})"


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return '\u265D'

    def can_move(self, board, row, col, row1, col1):
        if not (correct_coords(row1, col1) and (row != row1 and col != col1)
                and abs(col - col1) == abs(row - row1)):
            return False
        if board.field[row1][col1] is not None and board.field[row1][col1].get_color()\
                == board.field[row][col].get_color():
            return False
        coords = []
        if row1 < row and col1 > col:
            coords = [(row - i, col + i) for i in range(1, 9) if row - i >= row1 and col + i <= col1]
            coords.remove((row1, col1))
        elif row1 > row and col1 > col:
            coords = [(row + i, col + i) for i in range(1, 9) if row + i <= row1 and col + i <= col1]
            coords.remove((row1, col1))
        elif row1 > row and col1 < col:
            coords = [(row + i, col - i) for i in range(1, 9) if row + i <= row1 and col - i >= col1]
            coords.remove((row1, col1))
        elif row1 < row and col1 < col:
            coords = [(row - i, col - i) for i in range(1, 9) if row - i >= row1 and col - i >= col1]
            coords.remove((row1, col1))
        for i in range(len(board.field)):
            for j in range(len(board.field[i])):
                if board.field[i][j] is not None:
                    if (i, j) in coords:
                        return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __repr__(self):
        return f"Bishop({self.color})"


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return '\u265B'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if Rook(self.color).can_move(board, row, col, row1, col1)\
                or Bishop(self.color).can_move(board, row, col, row1, col1):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __repr__(self):
        return f"Queen({self.color})"


class Rook:
    def __init__(self, color):
        self.color = color
        self.flag_for_cast = True

    def char(self):
        return '\u265C'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if row != row1 and col != col1 and correct_coords(row1, col1):
            return False
        if board.field[row1][col1] is not None and board.field[row1][col1].get_color()\
                == board.field[row][col].get_color():
            return False
        coords = []
        if row1 < row and col1 == col:
            coords = [(row - i, col) for i in range(1, 9) if row - i >= row1]
            coords.remove((row1, col1))
        elif row1 > row and col1 == col:
            coords = [(row + i, col) for i in range(1, 9) if row + i <= row1]
            coords.remove((row1, col1))
        elif row1 == row and col1 < col:
            coords = [(row, col - i) for i in range(1, 9) if col - i >= col1]
            coords.remove((row1, col1))
        elif row1 == row and col1 > col:
            coords = [(row, col + i) for i in range(1, 9) if col + i <= col1]
            coords.remove((row1, col1))
        for i in range(len(board.field)):
            for j in range(len(board.field[i])):
                if board.field[i][j] is not None:
                    if (i, j) in coords:
                        return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __repr__(self):
        return f"Rook({self.color})"


class Pawn:
    def __init__(self, color):
        self.color = color
        self.flag_for_pass = False

    def char(self):
        return '\u265F'

    def get_color(self):
        return self.color

    def can_taking_pass(self, board, row, col, row1, col1):
        direction = 1 if self.color == BLACK else -1
        var = ['col + 1 if col + 1 < 8 else col', 'col - 1 if col + 1 >= 0 else col']
        right_pawn = board.field[row][eval(var[0])]
        left_pawn = board.field[row][eval(var[1])]
        if not (row + direction == row1 and ((col + 1 == col1 and type(right_pawn) is Pawn)
                                             or (col - 1 == col1 and type(left_pawn) is Pawn))):
            return False
        if not (type(right_pawn) is Pawn and right_pawn.get_color() != self.get_color() or
                type(left_pawn) is Pawn and left_pawn.get_color() != self.get_color()):
            return False
        if abs(col - col1) == 1 and board.previous_move_for_pass and board.field[row1][col1] is None\
                and board.field[board.pass_figure[0]][board.pass_figure[1]].get_color() != self.get_color():
            return True
        return False

    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False
        if self.color == BLACK:
            start_row, direction = 1, 1
        else:
            start_row, direction = 6, -1
        if (row1 - row) * direction == 1 and board.field[row1][col1] is None:
            self.flag_for_pass = False
            return True
        if start_row == row and board.field[row + direction][col1] is None and row + 2 * direction == row1:
            self.flag_for_pass = True
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        if board.field[row1][col1] is not None and board.field[row1][col1].get_color()\
                == board.field[row][col].get_color():
            return False
        if board.field[row1][col1] is None:
            return False
        direction = 1 if self.color == BLACK else -1
        if row + direction == row1 and (col + 1 == col1 or col - 1 == col1):
            self.flag_for_pass = False
            return True
        return False

    def __repr__(self):
        return f"Pawn({self.color})"


class King:
    def __init__(self, color):
        self.color = color
        self.flag_for_cast = True

    def char(self):
        return '\u265A'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not (correct_coords(row1, col1)):
            return False
        if board.field[row1][col1] is not None and board.field[row1][col1].get_color()\
            == board.field[row][col].get_color():
            return False
        coords = [(row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1),
                  (row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]
        return (row1, col1) in list(filter(lambda x: 0 <= x[0] < 8 and 0 <= x[1] < 8, coords))

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def __repr__(self):
        return f"King({self.color})"
