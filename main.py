import pygame

import globals as G
from Board import Board, BoardSize


def main():
    pygame.init()

    WINDOW = pygame.display.set_mode(
        (G.VIRTUALWIDTH, G.VIRTUALHEIGHT),
        pygame.RESIZABLE
    )

    brodie: pygame.Surface = pygame.image.load("images/brodie.png")
    brodie = pygame.transform.scale(brodie, (500,500))

    BOARD = Board()
    BOARD.newBoard(brodie, BoardSize.SMALL)

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

        WINDOW.fill((124,124,124,255))
        BOARD.render(WINDOW)
        pygame.display.flip()

        clock.tick(FPS)
        # print(f"{clock.get_fps():.2f}")

    pygame.quit()

if __name__ == "__main__":
    main()