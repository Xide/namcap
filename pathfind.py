from map import Map

class PathFinder:

    DFL_WEIGHT = 42
    LIMIT = 100000

    def __init__(self, map: Map):
        self.map = map
        self.explored = None

    def _pf(self, source: tuple, dest: tuple, avoids:list):
        if source == dest:
            return
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) + abs(y) != 1:
                    continue
                tmp = x + source[0], y + source[1]
                if self.map[tmp] in avoids:
                    continue
                if self.explored[source] + 1 < self.explored[tmp]:
#                    print(self.explored[source] + 1, self.explored[tmp])
                    self.explored[tmp] = self.explored[source] + 1
                    self._pf(tmp, dest, avoids)


    def reverse_path(self, source):
        if self.explored[source] == PathFinder.LIMIT:
            #print('Impossible path')
            return None
        #print('Objective is %d steps ahead' % self.explored[source])
        path = []

        while self.explored[source]:
            min, coord = PathFinder.LIMIT, (0, 0)

            for x in range(-1, 2):
                for y in range(-1, 2):
                    if abs(x) + abs(y) != 1:
                        continue
                    tmp = x + source[0], y + source[1]
                    if self.map[tmp] == Map.WALL:
                        continue
                    if min > self.explored[tmp]:
                        min = self.explored[tmp]
                        coord = tmp
            path.append(coord)
            source = coord
        return path


    def find(self, source: tuple, dest:tuple, avoids:list=None):
        if avoids is None:
            avoids = [Map.WALL]
        if self.active:
            raise RuntimeError('Pathfinder double execution')
        self.setUp()
        self.explored[dest] = 0
        self._pf(dest, source, avoids)
        result = self.reverse_path(source)
        self.tearDown()
        return result


    def setUp(self):
        self.explored = self.map.copy()
        for x in range(self.map.x):
            for y in range(self.map.y):
                if self.map[(x, y)] != Map.WALL:
                    self.explored[(x, y)] = PathFinder.LIMIT

    def tearDown(self):
        del self.explored
        self.explored = None

    @property
    def active(self):
        return not (self.explored is None)
