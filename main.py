# main.py

import pygame

import globals as G
from MainMenu import MenuManager
from Board import Board

def main():
    pygame.init()

    WINDOW = pygame.display.set_mode(
        (G.VIRTUALWIDTH, G.VIRTUALHEIGHT)
    )

    MENUMANAGER = MenuManager()
    BOARD = Board()

    clock = pygame.time.Clock()
    FPS = 60

    while G.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                G.toggleRunning()

            if G.gamestate == G.GameState.Playing:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousePos = event.pos

                        for piece in reversed(BOARD.pieceDraggables):
                            if piece.contains(mousePos):
                                BOARD.activePiece = piece
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        piece = BOARD.activePiece

                        if piece is not None:
                            if piece.closeToFather():
                                piece.fatherPiece.shouldShow = True
                                BOARD.pieceDraggables.remove(piece)

                        BOARD.activePiece = None

            elif G.gamestate == G.GameState.Menu:
                MENUMANAGER.handleInput(event)

        if G.gamestate == G.GameState.Playing:
            BOARD.update()


        WINDOW.fill((124,124,124,255))
        if G.gamestate == G.GameState.Playing:
            BOARD.render(WINDOW)
        elif G.gamestate == G.GameState.Menu:
            MENUMANAGER.render(WINDOW)
        
        pygame.display.flip()


        clock.tick(FPS)
        print(f"{clock.get_fps():.2f}")

    pygame.quit()

if __name__ == "__main__":
    main()