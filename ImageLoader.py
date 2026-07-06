import pygame
import os

class ImageLoader:
    _instance = None

    __slots__ = (
        "images"
    )

    def __init__(self) -> None:
        if not hasattr(self, "images"):
            self.images: dict[str, pygame.Surface] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def loadImages(self) -> None:
        folder: str = "images"

        if not os.path.exists(folder):
            return

        for file in os.listdir(folder):
            if not file.lower().endswith(".png"):
                continue
            
            self.addImage(file)

    def addImage(self, name: str) -> None:
        folder: str = "images"

        path: str = os.path.join(folder, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Asset file not found at path: {path}")

        img = pygame.image.load(path).convert_alpha()
        name = os.path.splitext(name)[0]
        self.images[name] = img

    def getImage(self, name: str) -> pygame.Surface | None:
        if name not in self.images:
            raise RuntimeError(f"Image '{name}' does not exist in memory.")
        return self.images.get(name)
    
    def removeImage(self, name: str) -> None:
        if name not in self.images:
            raise RuntimeError(f"Image '{name}' does not exist in memory.")
        self.images.pop(name, None)