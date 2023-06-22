from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:

    def __init__(self):
        self.squares =[[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.next_turn = 'white'
        self.last_move = None

    def move(self, piece, move):

        #EN PASSANT
        if isinstance(piece, Pawn):
            if self.check_enpassant(piece, move):
                self.squares[move.initial.row][move.final.col].piece = None
                piece.en_passant = False

        #MOVING
        self.squares[move.initial.row][move.initial.col].piece = None
        self.squares[move.final.row][move.final.col].piece = piece

        #PROMOTION
        if isinstance(piece, Pawn):
            self.check_promotion(piece.color, move.final)

        #CASTLING
        if isinstance(piece, King):
            if self.castling(move.initial, move.final):
                diff = move.final.col - move.initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
                self.next_turn = piece.color

        piece.moved = True
        piece.clear_moves()

        self.last_move = move
        self.next_move()

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, color, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(color)

    def check_enpassant(self, piece, move):
        #Checking if its moving diagonally and if the final square does not have a piece
        if (not move.final.has_piece()) and (abs(move.final.col - move.initial.col) == 1) and piece.en_passant == True:
            return True
        return False
    
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(temp_piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False


    def castling(self, inital, final):
        return abs(inital.col - final.col) == 2

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

    def calc_moves(self, piece, row, col, bool = True):
        
        def king_moves():

            #Normal moves
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
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)

                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            #Castling
            if not piece.moved:
                left_rook = self.squares[row][0].piece
                right_rook = self.squares[row][7].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        castle_enable = True
                        for c in range(1, 4):
                            if c>2:
                                i = Square(row, col)
                                f = Square(row, c)
                                m = Move(i, f)
                                if not self.valid_move(piece, m):
                                    castle_enable = False
                            if self.squares[row][c].has_piece():
                                castle_enable = False
                        
                        if castle_enable:
                            piece.left_rook = left_rook

                            initial = Square(row, 0)
                            final = Square(row, 3)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(left_rook, move):
                                    left_rook.add_move(move)
                            else:
                                left_rook.add_move(move)

                            initial = Square(row, col)
                            final = Square(row, 2)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if c<6:
                                i = Square(row, col)
                                f = Square(row, c)
                                m = Move(i, f)
                                if not self.valid_move(piece, m):
                                    break
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                piece.right_rook = right_rook

                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(right_rook, move):
                                        right_rook.add_move(move)
                                else:
                                    right_rook.add_move(move)

                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, move):
                                        piece.add_move(move)
                                else:
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
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)

                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def pawn_moves():

            #Removing en passant if it was available before
            if piece.en_passant == True:
                piece.moves.pop()
                piece.en_passant = False

            #Vertical moves
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (steps + 1))

            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
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
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            #En Passant
            if self.last_move is not None:
                last_initial = self.last_move.initial
                last_final = self.last_move.final

                #Check if last move was a double move pawn
                if isinstance(self.squares[last_final.row][last_final.col].piece, Pawn) and abs(last_initial.row - last_final.row) == 2:
                    #Check if it is enemy pawn moved beside THE pawn
                    if row == last_final.row and abs(col - last_final.col) == 1 and (last_final.piece.color != piece.color):
                        #Add move
                        initial = Square(row, col)
                        final = Square(row + piece.dir, last_final.col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                                piece.en_passant = True
                        else:
                            piece.add_move(move)
                            piece.en_passant = True


        def straightline_moves(incrs):
                
            for incr in incrs:
                initial = Square(row, col)
                row_incr, col_incr = incr
                move_row = row + row_incr
                move_col = col + col_incr

                while Square.in_range(move_row, move_col):
                    final_piece = self.squares[move_row][move_col].piece
                    final = Square(move_row, move_col, final_piece)
                    move = Move(initial, final)
                    #team
                    if self.squares[move_row][move_col].has_team_piece(piece.color):
                        break
                    
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
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