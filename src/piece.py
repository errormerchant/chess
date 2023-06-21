import os

class Piece:

    def __init__(self, name, value, color, texture = None, texture_rect = None):
        self.name = name
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.color = color
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size = 80):
        self.texture = os.path.join(
            f'assets\\images\\imgs-{size}px\\{self.color}_{self.name}.png'
        )

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', 1.0, color)

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', 3.0, color)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', 3.0001, color)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', 5.0, color)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', 9.0, color)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', 99999.0, color)