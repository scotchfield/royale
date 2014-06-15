import random

ITEM_T = ['weapon']

def item(n, t, dmg_n, dmg_d, dist) :
    if t not in ITEM_T:
        print('WARNING ({0}): {1} not valid type'.format(n, t))
    return {
        'name': n,
        'type': t,
        'dmg_n': dmg_n,
        'dmg_d': dmg_d,
        'distance': dist,
    }

ITEM_OBJ = {
    'pistol': item('Pistol', 'weapon', 3, 20, 8),

}

class World():

    def __init__(self):
        self.__tiles = []
        self.__items = []
        self.__characters = [] # for blocking, not trusted data

    def __str__(self):
        st = ''
        for y in range(len(self.__tiles)):
            for x in range(len(self.__tiles[y])):
                t = self.is_character_at(x, y)
                if t:
                    st = '{0}{1}'.format(st, t[2]['c'])
                    continue
                t = self.is_item_at(x, y)
                if t:
                    st = '{0}{1}'.format(st, '*')
                    continue
                st = '{0}{1}'.format(st, self.get(x, y))
            st = '{0}\n'.format(st)
        st = '{0}{1}'.format(st, self.__items)
        return st

    def randomize(self, x, y, n):
        self.__x = x
        self.__y = y
        for i in range(y):
            self.__tiles.append(['.'] * x)
        for i in range(n):
            self.__items.append(
                (random.randint(0, x), random.randint(0, y),
                 random.choice(ITEM_OBJ.keys())))

    def copy(self, w, x, y, visibility):
        size = visibility * 2 + 1
        self.__x = size
        self.__y = size
        self.__tiles = []
        x_min = x - visibility
        x_max = x + visibility
        y_min = y - visibility
        y_max = y + visibility
        for j in range(size):
            row = []
            for i in range(size):
                row.append(w.get(i + x_min, j + y_min))
            self.__tiles.append(row)
        for t in w.__items:
            if (t[0] >= x_min) and (t[0] <= x_max) and (t[1] >= y_min) and (t[1] <= y_max):
                print(t)
                print(x, y, visibility)
                self.__items.append(t) # TODO NOT CORRECT LOCATION IN REMAPPING
        for t in w.__characters:
            print(t)
            if (t[0] >= x_min) and (t[0] <= x_max) and (t[1] >= y_min) and (t[1] <= y_max):
                self.__characters.append(t) # TODO NOT CORRECT LOCATION IN REMAPPING

    def get(self, x, y):
        if y >= 0 and y < len(self.__tiles):
            if x >= 0 and x < len(self.__tiles[y]):
                return self.__tiles[y][x]
        return '#'

    def get_local(self, x, y, visibility):
        w = World()
        w.copy(self, x, y, visibility)
        return w

    def is_blocked(self, x, y):
        if x < 0 or x >= self.__x:
            return True
        if y < 0 or y >= self.__y:
            return True
        if self.get(x, y) in ['#']:
            return True
        return False

    def is_empty(self, x, y):
        if self.is_blocked(x, y):
            return False
        for t in self.__items:
            if t[0] == x and t[1] == y:
                return False
        for t in self.__characters:
            if t[0] == x and t[1] == y:
                return False
        return True

    def get_empty(self):
        done = False
        while True: # TODO this could be infinite, cut off after some point
            x = random.randint(0, self.__x)
            y = random.randint(0, self.__y)
            if self.is_empty(x, y):
                return (x, y)
            
    def add_character(self, x, y, state): # TODO not sufficient now, need state
        self.__characters.append((x, y, state))

    def reset_characters(self):
        self.__characters = []

    def is_item_at(self, x, y):
        for t in self.__items:
            if t[0] == x and t[1] == y:
                return t
        return False

    def is_character_at(self, x, y):
        for t in self.__characters:
            if t[0] == x and t[1] == y:
                return t
        return False
