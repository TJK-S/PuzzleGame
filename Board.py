import pygame

import globals as G

from Piece import PieceDraggable, GridPiece
from random import getrandbits
from enum import Enum

class BoardSize(Enum):
    TINY = (2, 2)
    SMALL = (4, 4)
    MEDIUM = (8, 8)
    LARGE = (16, 16)

class Board:
    _instance = None

    __slots__ = (
        "gridSize", 
        "pieces", "pieceDraggables",
        "activePiece",
        "imageSize", "cellSize", "startPos"
    )

    GAP: int = 6

    def __init__(self) -> None:
        self.gridSize: tuple[int, int] = (-1, -1)
        self.pieces: list[GridPiece] = []
        
        self.pieceDraggables: list[PieceDraggable] = []
        self.activePiece: PieceDraggable | None = None

        self.imageSize: tuple[int, int] = (-1, -1)
        self.cellSize: tuple[int, int] = (-1, -1)
        self.startPos: tuple[int, int] = (-1, -1)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def newBoard(self, image: pygame.Surface, size: BoardSize | None, customSize: tuple[int, int] | None = None) -> None:
        if (size is None) == (customSize is None):
            raise ValueError(
                "Board.newBoard | Exactly one of 'size' or 'customSize' must be specified."
            )

        if size is not None:            
            self.gridSize = size.value

        if customSize:
            self.gridSize = customSize

        self.pieces.clear()
        self.pieceDraggables.clear()
        self.imageSize = image.get_size()

        # will need to create a new image from given image thats dimensions
        # divide evenly with the given gridSize
        # use the data from the created image to give to the fatherPieces (Piece Objects)
        # basically every piece will get portions of the loaded image

        cellWidth = self.imageSize[0] // self.gridSize[0]
        cellHeight = self.imageSize[1] // self.gridSize[1]

        self.cellSize = (cellWidth, cellHeight)
        G.setPieceSize(self.cellSize)

        for y in range(self.gridSize[1]):
            for x in range(self.gridSize[0]):
                rect = pygame.Rect(x * cellWidth, y * cellHeight, cellWidth, cellHeight)
                self.pieces.append(GridPiece((x, y), image.subsurface(rect)))

        board_width = self.gridSize[0] * cellWidth + (self.gridSize[0] - 1) * Board.GAP
        board_height = self.gridSize[1] * cellHeight + (self.gridSize[1] - 1) * Board.GAP

        start_x = (G.VIRTUALWIDTH - board_width) // 2
        start_y = (G.VIRTUALHEIGHT - board_height) // 2
        
        self.startPos = (start_x, start_y)

        for y in range(self.gridSize[1]):
            for x in range(self.gridSize[0]):
                piece = self.get((x, y))
                
                piece.pixelPos = (
                    start_x + x * (cellWidth + Board.GAP),
                    start_y + y * (cellHeight + Board.GAP),
                )

                piece.leftEdge  = (x == 0)
                piece.rightEdge = (x == self.gridSize[0] - 1)
                piece.upEdge    = (y == 0)
                piece.downEdge  = (y == self.gridSize[1] - 1)

                if not piece.leftEdge:
                    left = self.get((x - 1, y))
                    piece.leftBlank = not left.rightBlank

                if not piece.upEdge:
                    above = self.get((x, y - 1))
                    piece.upBlank = not above.downBlank

                if not piece.rightEdge:
                    piece.rightBlank = bool(getrandbits(1))

                if not piece.downEdge:
                    piece.downBlank = bool(getrandbits(1))
                
                self.pieceDraggables.append(
                    PieceDraggable(
                        (x, y),
                        piece
                    )
                )

    def get(self, pos: tuple[int, int]) -> GridPiece:
        x, y = pos
        width, height = self.gridSize

        if not (0 <= x < width and 0 <= y < height): 
            raise IndexError(
                f"Board.get | Position {pos} is out of bounds for grid size {self.gridSize}"
            )
        return self.pieces[y * width + x]
    
    def update(self) -> None:
        if self.activePiece:
            self.activePiece.update()

    def render(self, surface: pygame.Surface) -> None:
        for piece in self.pieces:
            if piece.shouldShow:
                piece.render(surface)

        for piece in self.pieceDraggables:
            piece.render(surface)

        cols, rows = self.gridSize
        cell_w, cell_h = self.cellSize
        start_x, start_y = self.startPos

        color = (200, 200, 200)  # light gray grid lines

        for x in range(cols + 1):
            px = start_x + x * (cell_w + self.GAP) - self.GAP // 2
            pygame.draw.line(
                surface,
                color,
                (px, start_y),
                (px, start_y + rows * (cell_h + self.GAP) - self.GAP),
                1
            )

        for y in range(rows + 1):
            py = start_y + y * (cell_h + self.GAP) - self.GAP // 2
            pygame.draw.line(
                surface,
                color,
                (start_x, py),
                (start_x + cols * (cell_w + self.GAP) - self.GAP, py),
                1
            )