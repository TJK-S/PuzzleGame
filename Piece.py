import pygame
from random import randint
from enum import Enum

import globals as G

class EdgeType(Enum):
    FLAT = 0
    TAB = 1
    BLANK = 2

class GridPiece:
    
    __slots__ = {
        "up", "down", "left", "right",
        "shouldShow",
        "gridPos", "pixelPos",
        "image"
    }
    
    def __init__(self, pos: tuple[int, int], image: pygame.Surface) -> None:

        self.up = self.down = self.left = self.right = EdgeType.FLAT 

        # bool for if piece should render
        # true only when associating draggable is "inserted"
        self.shouldShow: bool = False

        self.gridPos: tuple[int, int] = pos
        self.pixelPos: tuple[int, int] = (-1, -1) #Initialized in Board.newBoard()

        self.image: pygame.Surface = image
    
    def render(self, surface: pygame.Surface) -> None:
        if not self.shouldShow:
            return
        
        x, y = self.pixelPos

        # def draw_edge(is_blank: bool, edge: str):
        #     color = (255, 0, 100) if is_blank else (0, 255, 100)

        #     if edge == "left":
        #         pygame.draw.line(surface, color, (x, y), (x, y + G.pieceSize[1]), 4)
        #     elif edge == "right":
        #         pygame.draw.line(surface, color, (x + G.pieceSize[0], y), (x + G.pieceSize[0], y + G.pieceSize[1]), 4)
        #     elif edge == "up":
        #         pygame.draw.line(surface, color, (x, y), (x + G.pieceSize[0], y), 4)
        #     elif edge == "down":
        #         pygame.draw.line(surface, color, (x, y + G.pieceSize[1]), (x + G.pieceSize[0], y + G.pieceSize[1]), 4)

        # pygame.draw.rect(
        #     surface,
        #     (12, 120, 120),
        #     (x, y, G.pieceSize[0], G.pieceSize[1]),
        # )

        surface.blit(
            self.image, 
            (x, y)
        )

        # draw_edge(self.leftBlank, "left")
        # draw_edge(self.rightBlank, "right")
        # draw_edge(self.upBlank, "up")
        # draw_edge(self.downBlank, "down") 

class PieceDraggable():

    __slots__ = (
        "pos", "pixelPos",
        "fatherPiece"
    )

    def __init__(self, pos: tuple[int, int], fatherPiece: GridPiece) -> None:

        self.pos = pos 
        self.pixelPos: tuple[int, int] = (
            randint(0, G.VIRTUALWIDTH), 
            randint(0, G.VIRTUALHEIGHT)
        )

        self.fatherPiece: GridPiece = fatherPiece
        
    def update(self) -> None:
        x, y = pygame.mouse.get_pos()
        self.pixelPos = (
            x - G.pieceSize[0] // 2,
            y - G.pieceSize[1] // 2
        )

    def render(self, surface: pygame.Surface) -> None:
        x, y = self.pixelPos

        # def draw_edge(is_blank: bool, edge: str):
        #     color = (255, 0, 0) if is_blank else (0, 255, 0)

        #     if edge == "left":
        #         pygame.draw.line(surface, color, (x, y), (x, y + G.pieceSize[1]), 4)
        #     elif edge == "right":
        #         pygame.draw.line(surface, color, (x + G.pieceSize[0], y), (x + G.pieceSize[0], y + G.pieceSize[1]), 4)
        #     elif edge == "up":
        #         pygame.draw.line(surface, color, (x, y), (x + G.pieceSize[0], y), 4)
        #     elif edge == "down":
        #         pygame.draw.line(surface, color, (x, y + G.pieceSize[1]), (x + G.pieceSize[0], y + G.pieceSize[1]), 4)

        # pygame.draw.rect(
        #     surface,
        #     (120, 12, 120),
        #     (x, y, G.pieceSize[0], G.pieceSize[1])
        # )


        fp = self.fatherPiece

        surface.blit(
            fp.image, 
            (x, y)
        )

        # draw_edge(fp.leftBlank, "left")
        # draw_edge(fp.rightBlank, "right")
        # draw_edge(fp.upBlank, "up")
        # draw_edge(fp.downBlank, "down")

    def contains(self, mousePos: tuple[int, int]) -> bool:
        mx, my = mousePos
        x, y = self.pixelPos

        return (x <= mx < x + G.pieceSize[0] and y <= my < y + G.pieceSize[1])
    
    def closeToFather(self) -> bool:
        LENIENCY = max(G.pieceSize[0], G.pieceSize[1]) // 2

        px, py = self.pixelPos
        fx, fy = self.fatherPiece.pixelPos

        piece_center = (
            px + G.pieceSize[0] // 2,
            py + G.pieceSize[1] // 2,
        )

        father_center = (
            fx + G.pieceSize[0] // 2,
            fy + G.pieceSize[1] // 2,
        )

        return (
            abs(piece_center[0] - father_center[0]) <= LENIENCY and
            abs(piece_center[1] - father_center[1]) <= LENIENCY
        )