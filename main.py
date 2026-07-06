import pygame

import globals as G
from Board import Board, BoardSize


def main():
    pygame.init()

    brodie: pygame.Surface = pygame.image.load("images/animal.png")
    brodie = pygame.transform.scale(brodie, (600,500))

    BOARD = Board()
    BOARD.newBoard(brodie, BoardSize.MEDIUM)

    WINDOW = pygame.display.set_mode(
        (G.VIRTUALWIDTH, G.VIRTUALHEIGHT),
        pygame.RESIZABLE
    )

    clock = pygame.time.Clock()
    FPS = 60
    running = True

    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False

                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousePos = event.pos

                        for piece in reversed(BOARD.pieceDraggables):
                            if piece.contains(mousePos):
                                BOARD.activePiece = piece
                                break

                case pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        piece = BOARD.activePiece

                        if piece is not None:
                            if piece.closeToFather():
                                piece.fatherPiece.shouldShow = True
                                BOARD.pieceDraggables.remove(piece)

                        BOARD.activePiece = None

                case _: pass

        BOARD.update()

        WINDOW.fill((0,0,0,255))
        BOARD.render(WINDOW)
        pygame.display.flip()

        clock.tick(FPS)
        # print(f"{clock.get_fps():.2f}")

    pygame.quit()

main()