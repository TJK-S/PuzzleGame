VIRTUALWIDTH = 1280
VIRTUALHEIGHT = 720

pieceSize: tuple[int, int] = (50, 50)
def setPieceSize(size: tuple[int, int]):
    global pieceSize
    pieceSize = size