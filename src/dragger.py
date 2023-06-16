import pygame

from const import *

class Dragger:

    def __init__(self):
        self.mousex = 0
        self.mousey = 0
        self.initial_row = 0
        self.inital_col = 0
        self.dragging = False
        self.piece = None

    def update_blit(self, surface):
        self.piece.set_texture(size = 128)
        texture = self.piece.texture
        #img
        img = pygame.image.load(texture)
        #img_center
        img_center = (self.mouseX, self.mouseY)
        #texture_rect
        self.piece.texture_rect = img.get_rect(center = img_center)
        #blit
        surface.blit(img, self.piece.texture_rect)


    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.inital_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        if self.piece != None:
            self.piece.set_texture()
        self.piece = None
        self.dragging = False