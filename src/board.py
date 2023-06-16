from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares =[[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.next_turn = 'white'
        self.last_move = None

    def move(self, piece, move):
        self.squares[move.initial.row][move.initial.col].piece = None
        self.squares[move.final.row][move.final.col].piece = piece

        piece.moved = True
        piece.clear_moves()

        self.last_move = move
        self.next_move()

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def next_move(self):
        self.next_turn = 'white' if self.next_turn == 'black' else 'black'

    def _create(self):
        #Creating empty squares
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        (row_pawn, row_other) = (1, 0) if color == 'black' else (6, 7)

        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, piece, row, col):
        
        def king_moves():
            possible_moves = [
                (row-1, col+1),
                (row-1, col-1),
                (row+1, col+1),
                (row+1, col-1),
                (row+1, col),
                (row-1, col),
                (row, col+1),
                (row, col-1)
            ]

            for move in possible_moves:
                move_row, move_col = move

                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_has_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)

                        move = Move(initial, final)

                        piece.add_move(move)


        def knight_moves():
            possible_moves = [
                (row-2, col+1),
                (row-2, col-1),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row+1, col+2),
                (row-1, col-2),
                (row-1, col+2)
            ]

            for move in possible_moves:
                move_row, move_col = move

                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_has_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)

                        move = Move(initial, final)

                        piece.add_move(move)

        def pawn_moves():
            #Verical moves
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (steps + 1))

            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break

            #Diagonal moves
            move_row = row + piece.dir
            move_cols = [col - 1, col + 1]

            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move = Move(initial, final)
                        piece.add_move(move)



        def straightline_moves(incrs):
                
            for incr in incrs:
                initial = Square(row, col)
                row_incr, col_incr = incr
                move_row = row + row_incr
                move_col = col + col_incr

                while Square.in_range(move_row, move_col):
                    final = Square(move_row, move_col)
                    move = Move(initial, final)
                    #team
                    if self.squares[move_row][move_col].has_team_piece(piece.color):
                        break
                    
                    piece.add_move(move)
                    #enemy
                    if self.squares[move_row][move_col].has_enemy_piece(piece.color):
                        break
                        
                    #empty
                    else:
                        move_row = move_row + row_incr
                        move_col = move_col + col_incr
                    

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight): 
            knight_moves()
        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
        elif isinstance(piece, Rook):
            straightline_moves([
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ])
        elif isinstance(piece, King):
            king_moves()