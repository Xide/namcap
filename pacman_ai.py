from ai import AI
from map import Map
from math import sqrt
from controller import IController

def dist(source: tuple, dest: tuple):
    return sqrt((dest[0] - source[0]) ** 2 + (dest[1] - source[1]) ** 2)

class PacmanAI(AI):
    def __init__(self):
        self.it = None

    # def bn(self, map, pos, out={}):
    #     name = str(pos)
    #     if name in out:
    #         return
    #     out[name] = {}
    #     if map[pos] != Map.EMPTY:
    #         return
    #
    #
    #     res = {}
    #     for x in range(-1, 2):
    #         for y in range(-1, 2):
    #             if abs(x) + abs(y) == 1:
    #                 p2 = pos[0] + x, pos[1] + y
    #                 res[str(p2)] = 1
    #                 self.bn(map, p2, out)
    #     out[name] = res
    #
    # def pathfind(self, map, source, dest):
    #
    #     from dj import shortestPath
    #     res = {}
    #     self.bn(map, source, res)
    #     print(res)
    #     if str(dest) in res:
    #         res = shortestPath(res, str(source), str(dest))
    #     else:
    #         print('FUCK OFF ')
    #         return []
    #
    #     return res
    #     iterate = []# Map(map.x, map.y)
    #     tmp, map[source] = map[source], Map.EMPTY
    #     res = self._pf(map, source, dest, iterate)
    #     print('from', source, 'to', dest, ':', res)
    #     print(map)
    #     print('-' * 50)
    #     mp = Map(map.x, map.y)
    #     for x, y in iterate:
    #         mp[(x, y)] = Map.ENEMY_SPAWN
    #     print(iterate
    #         )
    #     map[source] = tmp
    #     return res
    #
    #
    # def _pf(self, map, source, dest, iterate, depth=0):
    #     print(depth, source, map[source])
    #     if source in iterate or map[source] != Map.EMPTY:
    #         return []
    #     if source == dest:
    #         print('Yipeeee')
    #         return [dest]
    #
    #     iterate += [source]
    #     best = None
    #
    #     print('*' * 20)
    #     for x in range(-1, 2):
    #         for y in range(-1, 2):
    #             loc = (x + source[0], y + source[1])
    #             if abs(x) + abs(y) == 1: # and map[loc] == Map.EMPTY:
    #                 print('Trying something', loc, map[loc])
    #                 path = self._pf(map, loc, dest, iterate, depth=depth+1)
    #                 if path:
    #                     print('AHAHAH')
    #                     return [source] + path
    #                     # if (not best or len(path) < len(best)):
    #                     #     best = path
    #     if best:
    #         return [source] + best
    #     else:
    #         #iterate[source] = Map.EMPTY
    #         return []

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
        pacman, enemies = self.locate_players(map)
        move, best = None, 0
        assert map[pacman] == Map.PACMAN
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

        best, mv2 = 10000000, None
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) + abs(y) == 1:
                    pos = (pacman[0] + x, pacman[1] + y)
                    if map[pos] == Map.EMPTY:
                        score = dist(pos, move)
                        if score < best:
                            best = score
                            mv2 = (x, y)
        #print(move, best)
        #print('[PacmanAI]: Selected move', move)
        return IController.from_tuple(mv2)