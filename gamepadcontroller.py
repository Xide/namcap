from controller import IController
from pygame.locals import *
from pygame import joystick

class GamepadController(IController):
    def __init__(self, id=0):
        joystick.init()
        assert joystick.get_count()
        self.joystick = joystick.Joystick(id)
        self.joystick.init()
        self.ctab = {
            (0, -1): IController.LEFT,
            (0, 1): IController.RIGHT,
            (1, 0): IController.DOWN,
            (-1, 0): IController.UP
        }

    def pump(self, event) -> int:
        if event.type == JOYBUTTONDOWN:
            return IController.ACTION
        print([self.joystick.get_axis(i) for i in (0, 1)])
        coord = (round(self.joystick.get_axis(0)),
                 round(self.joystick.get_axis(1)))
        print(coord)
        if coord not in self.ctab:
            return None
        return self.ctab[coord]