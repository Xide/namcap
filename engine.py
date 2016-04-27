import pygame
from pygame import event, time
from pygame.locals import QUIT, USEREVENT
from controller import IController
from gamepadcontroller import GamepadController as Controller
from keyboardcontroller import KeyboardController as FallbackController
from map import Map
from pacman_ai import PacmanAI
from ghost_ai import GhostAI
from pathfind import PathFinder


class Engine:
    def load_joysticks(self):
        return []

    def __init__(self, x, y, **kw):
        self.x = x
        self.y = y
        numpass, numfail = pygame.init()
        if numfail:
            pygame.quit()
            raise RuntimeError('Could not initialize %d modules (%d pass)'
                               % (numfail, numpass))
        self.controllers = self.load_joysticks()
        if not len(self.controllers):
            self.controllers.append(FallbackController())
        self.players_pos = []
        self.map = Map(x, y)
        self.ais = []
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

    def update(self, event, position):
        ctab = IController.to_tuple_tab()
        if event in ctab:
            item = self.map[position]
            print(item)
            assert item in [Map.PACMAN, Map.GHOST]

            return self.map.move(position, (position[0] + ctab[event][0],
                                            position[1] + ctab[event][1]))
        else:
            return False

    def populate(self, ghostno):
        uid = 0
        for lno, line in enumerate(self.map):
            while Map.SPAWN in line:
                if ghostno:
                    ghostno -= 1
                    self.ais.append(GhostAI((line.index(Map.SPAWN), lno)))
                else:
                    self.players_pos.append((line.index(Map.SPAWN), lno))
                line[line.index(Map.SPAWN)] = Map.GHOST

            while Map.ENEMY_SPAWN in line:
                line[line.index(Map.ENEMY_SPAWN)] = Map.PACMAN
                self.ais.append(
                    PacmanAI((line.index(Map.PACMAN), lno)))

    def run(self):
        stop = False
        print(len(self.controllers))
        self.populate(3 - len(self.controllers))
        ticks = [IController.LEFT] * len(self.controllers)
        watchs = [IController.RIGHT] * len(self.controllers)

        pygame.time.set_timer(USEREVENT, 150)
        # tick, watch = (IController.LEFT, IController.RIGHT)
        tick_watcher = False
        while not stop:
            for ev in event.get():
                if ev.type == QUIT:
                    print('Shutdown required, exiting gracefully')
                    return 0
                if ev.type == USEREVENT:
                    tick_watcher = True
                    break

                for ctrl in self.controllers:
                    if ctrl.match_device(ev):
                        ev = ctrl.pump(ev)
                        if ev is not None:
                            ticks[self.controllers.index(ctrl)] = ev

            if tick_watcher:
                tick_watcher = False
                for id in range(len(ticks)):
                    if ticks[id]:
                        print(id, self.players_pos)
                        if not self.update(ticks[id], self.players_pos[id]):
                            if self.update(watchs[id], self.players_pos[id]):
                                self.players_pos[id] = self.players_pos[id][0] + IController.to_tuple(ticks[id])[0], \
                                                       self.players_pos[id][1] + IController.to_tuple(ticks[id])[1]
                        else:
                            watchs[id] = ticks[id]
                            self.players_pos[id] = self.players_pos[id][0] + IController.to_tuple(ticks[id])[0], \
                                                   self.players_pos[id][1] + IController.to_tuple(ticks[id])[1]

                for ai in self.ais:
                    ps = ai.position
                    print(type(ai), ai.position, self.map[ai.position])
                    if not self.update(ai.play(self.map), ps):
                        ai.position = ps
                self.flip()


if __name__ == '__main__':
    engine = Engine(30, 20, map='map.png')
    engine.run()
