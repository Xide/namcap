from controller import IController
from pathfind import PathFinder
from map import Map
import random


class GhostAI(IController):
    def __init__(self, position: tuple):
        self.position = position
        self.chasing = True
        self.turns = 0
        self.destination = None
        self.ticker = False

    @staticmethod
    def whereispacman(map):
        for nl, line in enumerate(map):
            if Map.PACMAN in line:
                return (line.index(Map.PACMAN), nl)

    def play(self, map):
        assert map[self.position] == Map.GHOST
        if self.destination and \
                        map[self.position[0] + self.destination[0],
                            self.position[1] + self.destination[1]] in [Map.GHOST, Map.WALL]:
            self.destination = None
            self.turns -= 2
        if self.chasing:
            self.turns += 1
            if self.turns >= 20:
                self.chasing = False
                self.ticker = True
            map[self.position] = Map.EMPTY
            # print(map, self.destination)
            path = PathFinder(map).find(self.position,
                                        GhostAI.whereispacman(map),
                                        avoids=[Map.WALL, Map.GHOST])
            map[self.position] = Map.GHOST
            if not path:
                self.chasing = False
                self.destination = None
                return self.play(map)
            else:
                res = IController.from_tuple((path[0][0] - self.position[0], path[0][1] - self.position[1]))
                self.position = path[0]
                return res

        if not self.destination:
            while not self.destination:
                ncoord = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
                if map[self.position[0] + ncoord[0],
                       self.position[1] + ncoord[1]] != Map.EMPTY:
                    continue
                self.destination = ncoord

        if self.turns > 0:
            self.position = self.position[0] + self.destination[0], \
                            self.position[1] + self.destination[1]
            return IController.from_tuple(self.destination)
        else:
            self.turns = 0
            self.chasing = True
            return self.play(map)
