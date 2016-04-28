from math import log10 as log
import png
import copy

class Map:
    EMPTY = 'E'
    ENEMY_SPAWN = 'D'
    SPAWN = 'S'
    PACMAN = 'P'
    GHOST = 'G'
    WALL = 'W'

    class GameEnded(Exception):
        pass

    class Color:
        EMPTY = 0 # black
        WALL = 255 # blue
        PLAYER_SPAWN = 255 << 8 # green
        ENEMY_SPAWN = 255 << 16 # red
        PACMAN = 0xFFFF00

        @staticmethod
        def to_char(color: int):
            ctab = {
                Map.Color.WALL: Map.WALL,
                Map.Color.ENEMY_SPAWN: Map.ENEMY_SPAWN,
                Map.Color.PLAYER_SPAWN: Map.SPAWN,
                Map.Color.EMPTY: Map.EMPTY
            }
            return ctab[color]

    @staticmethod
    def to_color(char: int):
        ctab = {
            Map.WALL: Map.Color.WALL,
            Map.ENEMY_SPAWN: Map.Color.ENEMY_SPAWN,
            Map.SPAWN: Map.Color.PLAYER_SPAWN,
            Map.EMPTY: Map.Color.EMPTY,
            Map.PACMAN: Map.Color.ENEMY_SPAWN,
            Map.GHOST: Map.Color.PLAYER_SPAWN
        }
        return ctab[char]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map = [[Map.EMPTY] * self.x] * self.y


    def load_from_png_file(self, path: str):
        with open(path, 'rb') as inp:
            reader = png.Reader(file=inp)
            data = reader.read()
            if data[0] != self.x or data[1] != self.y:
                raise ValueError('map size must be equal to the image currently loading')
            data = list(data[2])
            for y in range(self.y):
                line = []
                for x in range(self.x):
                    rgb = data[y][3 * x: (3 * x) + 3]
                    color = (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]
                    #print(x, y, 'px value:', rgb, color)
                    for item in (Map.Color.EMPTY, Map.Color.WALL, Map.Color.PLAYER_SPAWN, Map.Color.ENEMY_SPAWN):
                        if item == color:
                            line += [Map.Color.to_char(color)]
                            break
                self.map[y] = line
        return True

    def collide(self, source: tuple, dest:tuple):

        assert self[source] in (Map.PACMAN, Map.GHOST)
        if self[dest] == Map.EMPTY:
            return True
        elif self[dest] == Map.WALL:
            return False

        if self[source] == Map.GHOST and self[dest] == Map.PACMAN:
            raise Map.GameEnded('WON')
        elif self[source] == Map.GHOST and self[dest] == Map.GHOST:
            return False
        raise RuntimeError('On fout quoi la ?')

    def move(self, source: tuple, dest: tuple):
        if self[source] not in (Map.PACMAN, Map.GHOST):
            raise ValueError('Object %s at (%d, %d) is not movable' % (
                self[source], source[0], source[1]
            ))
        if (self[dest] != Map.EMPTY and not self.collide(source, dest)):
            return False
        #print("Moving '%s'%s to '%s'%s" % (self[source], source, self[dest], dest))
        self[source], self[dest] = self[dest], self[source]
        return True

    def copy(self):
        res = Map(self.x, self.y)
        res.map = copy.deepcopy(self.map)
        return res

    def __repr__(self):
        #lenght = log(max([max(self.map[y]) for y in range(self.y)]))
        return  '\n'.join(['%s%s' % (' ' * 2, repr(x)) for x in self.map])

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.map[item]
        elif isinstance(item, tuple):
            return self.map[item[1]][item[0]]
        raise ValueError

    def __setitem__(self, key: tuple, value):
        self[key[1]][key[0]] = value


if __name__ == '__main__':
    m = Map(30, 20)
    m.load_from_png_file('map.png')
    print(m)