from controller import IController
from pygame.locals import *

class KeyboardController(IController):
    def __init__(self):
        self.ctab = {
            K_SPACE: IController.ACTION,
            K_a: IController.UP,
            K_d: IController.DOWN,
            K_s: IController.RIGHT,
            K_w: IController.LEFT
        }

    def pump(self, event) -> int:
        if event.type == KEYDOWN and event.key in self.ctab:
            return self.ctab[event.key]
        return None

    def match_device(self, event) -> bool:
        return hasattr(event, 'unicode')