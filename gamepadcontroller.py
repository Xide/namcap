from controller import IController
from pygame.locals import *
from pygame import joystick
from map import Map

class GamepadController(IController):

    @staticmethod
    def joystick_number():
        return joystick.get_count()

    def __init__(self, id=0):
        joystick.init()
        assert joystick.get_count()
        self.joystick = joystick.Joystick(id)
        self.id = id
        self.joystick.init()
        self.ctab = {
            (0, -1): IController.LEFT,
            (0, 1): IController.RIGHT,
            (1, 0): IController.DOWN,
            (-1, 0): IController.UP
        }

    def pump(self, event) -> int:
        if event.type == JOYBUTTONDOWN:
            print(event.dict['button'])
            if event.dict['button'] == 6:
                raise Map.GameEnded('exited')
            return IController.ACTION
        coord = (round(self.joystick.get_axis(0)),
                 round(self.joystick.get_axis(1)))
        if coord not in self.ctab:
            return None
        r = self.ctab[coord]
        return self.ctab[coord]

    def match_device(self, event):
        try:
            return event.type == JOYAXISMOTION or event.type == JOYBUTTONDOWN
        except:
            return False