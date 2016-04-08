from controller import IController
from pygame.locals import *

class KeyboardController(IController):
    def __init__(self):
        self.ctab = {
            K_SPACE: IController.ACTION,
            K_a: IController.LEFT,
            K_d: IController.RIGHT,
            K_s: IController.DOWN,
            K_w: IController.UP
        }

    def pump(self, event) -> int:
        if event.type == KEYDOWN and event.key in self.ctab:
            return self.ctab[event.key]
        return None
