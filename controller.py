class IController:
    LEFT = 42
    RIGHT = 43
    UP = 44
    DOWN = 45
    ACTION = 46

    @staticmethod
    def to_tuple_tab():
        ctab = {
            IController.LEFT: (-0, -1),
            IController.RIGHT: (0, 1),
            IController.UP: (-1, 0),
            IController.DOWN: (1, 0)
        }
        return ctab

    @staticmethod
    def to_tuple(move: int):
        return IController.to_tuple_tab()[move]

    @staticmethod
    def from_tuple(coord: tuple):
        ctab = {
            (-0, -1): IController.LEFT,
            (0, 1): IController.RIGHT,
            (-1, 0): IController.UP,
            (1, 0): IController.DOWN
        }
        return ctab[coord]
    def __init__(self):
        pass

    def pump(self, event) -> int:
        """
        Used to turn a raw event into controller based event
        :param event: pygame event
        :return: one of LEFT, RIGHT, UP, DOWN, ACTION
        """
        pass
