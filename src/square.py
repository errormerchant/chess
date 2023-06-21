class Square:

    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None
    
    def isempty(self):
        return not self.has_piece()
    
    def has_team_piece(self, color):
        return self.has_piece() and color == self.piece.color
    
    def has_enemy_piece(self, color):
        return self.has_piece() and color != self.piece.color
    
    def isempty_or_has_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg>7 or arg<0:
                return False          
        return True
    
