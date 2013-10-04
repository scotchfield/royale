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
        self.__tiles = []
        self.__x = x
        self.__y = y
        for i in range(y):
            self.__tiles.append(['.'] * x)
        self.__items = []
        for i in range(n):
            self.__items.append(
                (random.randint(0, x), random.randint(0, y),
                 random.choice(ITEM_OBJ.keys())))
        self.__characters = [] # for blocking, not trusted data

    def get(self, x, y):
        if y >= 0 and y < len(self.__tiles):
            if x >= 0 and x < len(self.__tiles[y]):
                return self.__tiles[y][x]
        return '#'

    def get_local(self, x, y, visibility):
        st = ''
        for i in range(y - visibility, y + visibility + 1):
            for j in range(x - visibility, x + visibility + 1):
                st = '{0}{1}'.format(st, self.get(i, j))
            st = '{0}\n'.format(st)
        return st

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
