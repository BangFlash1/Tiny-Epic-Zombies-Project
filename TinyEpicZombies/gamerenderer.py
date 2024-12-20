import pygame, os
import numpy as np
from .constants import peNames, rotations, CW, CH, tlCoords
from .helperfunctions.deserialisers import deserializeTl
from .helperfunctions.roomrects import genRoomRects

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH = info.current_w
HEIGHT = info.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

class GameRenderer:
    def __init__(self):
        self.cw = CW*WIDTH
        self.ch = CH*HEIGHT
        self.gameboardImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        self.gameboardImg = pygame.transform.scale(self.gameboardImg, (WIDTH, HEIGHT))
        self.storeSurfaces = self.__genStoreSurfaces()
        

    def renderGameScreen(self):
        DISPLAY.blit(self.gameboardImg)
        self.__renderStores()
        self.__renderMovementOptions()

    def __genStoreSurfaces(self): #  returns a list of store surfaces
        storeSurfaces = []
        for i in range(9):
            pathEnd = peNames[i]
            rotation = rotations[i]
            img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "stores", f"{pathEnd}"))
            img = pygame.transform.scale(img, (self.cw, self.ch))
            img = pygame.transform.rotate(img, rotation)
            storeSurfaces.append(img)
        return storeSurfaces
    
    def __renderStores(self):
        for store in range(len(self.storeSurfaces)):
            DISPLAY.blit(self.storeSurfaces[store], tuple(np.multiply((WIDTH, HEIGHT), deserializeTl(store))))

    def __renderMovementOptions(self):
        rect = pygame.Rect(50,50,40,40)
        for store in range(0,9):
            for room in range(0,3):
                # coords = (store, room)
                # points = deserializeCollider(coords)
                # tl = ((tlCoords[store][0] + points[0][0]), (tlCoords[store][1] + points[0][1]))
                # rect.topleft = tl
                roomsLst = genRoomRects()
                rect = roomsLst[store][room]
                pygame.draw.rect(DISPLAY, (0,0,255), rect)