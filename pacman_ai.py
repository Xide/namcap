from ai import AI
from map import Map
from math import sqrt
from controller import IController
from pathfind import PathFinder

def dist(source: tuple, dest: tuple):
    return sqrt((dest[0] - source[0]) ** 2 + (dest[1] - source[1]) ** 2)

class PacmanAI(AI):
    def __init__(self, position: tuple):
        self.position = position

    def locate_players(self, map):
        threats = []
        pacpos = None
        for y, line in enumerate(map):
            for x, char in enumerate(line):
                assert map[(x, y)] == char
                if char == Map.GHOST:
                    threats += [(x, y)]
                elif char == Map.PACMAN:
                    pacpos = (x, y)
        return (pacpos, threats)

    def play(self, map):
        source, enemies = self.locate_players(map)
        move, best = None, 0
        assert map[source] == Map.PACMAN
        #print('[PacmanAI] Enemies position at ', enemies)
        for x in range(map.x):
            for y in range(map.y):
                if map[(x, y)] == Map.EMPTY:
                    score = [dist((x, y), e) for e in enemies]
                    if len(score):
                        score = min(score)
                    else:
                        score = -1
                    #print('[PacmanAI] Evaluating move', (x, y), ':', score)
                    if score > best:
                        best = score
                        move = (x, y)

        path = PathFinder(map).find(source, move, avoids=[Map.WALL, Map.GHOST])
        if path:
            self.position = path[0]
            return IController.from_tuple((path[0][0] - source[0], path[0][1] - source[1]))
        else:
            # TODO : retard style
            return None
