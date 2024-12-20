import os, json, pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH = info.current_w
HEIGHT = info.current_h

def deserializeRoom(coords):
    store, room = coords[0], coords[1]
    with open(os.path.join("TinyEpicZombies","jsonfiles", "roompoints.json")) as file:
        data = json.loads("".join(file.readlines()))
        return(data["stores"][f"store{store}"]["rooms"][f"room{room}"])

def deserializeTl(store):
    with open(os.path.join("TinyEpicZombies","jsonfiles", "roompoints.json")) as file:
        data = json.loads("".join(file.readlines()))
        return(tuple(data["stores"][f"store{store}"]["tl"]))