import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        pygame.display.set_caption('Chess')

    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_mouse(event.pos)
                dragger.update_blit(screen)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.drag_piece(piece)

                        if piece.color == board.next_turn:
                            board.calc_moves(piece, clicked_row, clicked_col, True)
                            dragger.save_initial(event.pos)                           

                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.inital_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                    
                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        screen = self.screen
                        board = self.game.board
                        dragger = self.game.dragger


                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
 
            pygame.display.update()


main = Main()
main.mainloop()