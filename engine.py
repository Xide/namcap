import pygame
from pygame import event, time
from pygame.locals import QUIT, USEREVENT
from controller import IController
from gamepadcontroller import GamepadController as Controller
from map import Map
from pacman_ai import PacmanAI


class Engine:
    def __init__(self, x, y, **kw):
        self.x = x
        self.y = y
        numpass, numfail = pygame.init()
        if numfail:
            pygame.quit()
            raise RuntimeError('Could not initialize %d modules (%d pass)'
                               % (numfail, numpass))
        self.controller = Controller()
        self.map = Map(x, y)
        self.ais = [PacmanAI()]
        if 'map' in kw:
            self.map.load_from_png_file(kw['map'])
        pygame.key.set_repeat(400, 30)  # TODO : regler valeurs
        self.display = pygame.display.set_mode((x * 50, y * 50))

    def flip(self):
        """
        """
        for x in range(self.x):
            for y in range(self.y):
                item = self.map[(x, y)]
                pygame.draw.circle(self.display, Map.to_color(item),
                                   ((50 * x) + 25, (50 * y) + 25), 23)
        pygame.display.flip()

    def __del__(self):
        pass

    def __repr__(self):
        pass

    def update(self, event, pacman=False):
        item = Map.PACMAN if pacman is True else Map.GHOST
        ctab = IController.to_tuple_tab()
        for idx, line in enumerate(self.map):
            if item in line:
                source = (line.index(item), idx)
        if event in ctab:
            return self.map.move(source, (source[0] + ctab[event][0],
                                   source[1] + ctab[event][1]))
        else:
            return False

    def populate(self):
        for line in self.map:
            while Map.SPAWN in line:
                line[line.index(Map.SPAWN)] = Map.GHOST
            while Map.ENEMY_SPAWN in line:
                line[line.index(Map.ENEMY_SPAWN)] = Map.PACMAN

    def run(self):
        stop = False
        self.populate()
        pygame.time.set_timer(USEREVENT, 150)
        tick, watch = (IController.LEFT, IController.RIGHT)
        tick_watcher = False
        while not stop:
            for ev in event.get():
                if ev.type == QUIT:
                    print('Shutdown required, exiting gracefully')
                    return 0
                if ev.type == USEREVENT:
                    tick_watcher = True
                    break
                ev = self.controller.pump(ev)
                if ev is not None:
                    tick = ev
            if ev and tick_watcher:
                tick_watcher = False
                for ai in self.ais:
                    self.update(ai.play(self.map), True)
                if not self.update(tick):
                    self.update(watch)
                    tick = watch
                self.flip()
                watch = tick



if __name__ == '__main__':
    engine = Engine(30, 20, map='map.png')
    engine.run()
