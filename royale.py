import random

from world import World

VERBOSE = True

AGENT_CHARS = ['!', '@', '$', '%', '^', '&', '(', ')']

AGENT_COMMANDS = [
    'pass',
    'north', 'south', 'east', 'west',
    'take',
]

def main():
    w = World()
    w.randomize(20, 12, 30)
    print(w)

    player_obj = [
        StumbleAgent(),
        StumbleAgent(),
        StumbleAgent(),
    ]

    state_obj = []
    for i in range(len(player_obj)):
        (x, y) = w.get_empty()
        state_obj.append(
            {
                'health': 100,            # 
                'stamina': 100,           # actions take stamina
                'initiative': 100,        # action priority
                'weapon_name': 'Unarmed', # optional? an agent might care
                'weapon_damage_n': 1,     # number of dice to roll
                'weapon_damage_d': 4,     # sides on each die (1d4 here)
                'visibility': 3,          # sight squares
                'x': x,                   # 
                'y': y,                   # 
                'inventory': [],          # 
                'c': random.choice(AGENT_CHARS),
            }
        )

    cycles_left = 3
    done = False
    while not done:
        if VERBOSE:
            print('# Cycle {0} #'.format(cycles_left))

        w.reset_characters()
        for i in range(len(player_obj)):
            w.add_character(state_obj[i]['x'], state_obj[i]['y'],
                            state_obj[i])
            # TODO obscure some of this state
            print(state_obj[i])

        print(w)

        action_obj = []
        for i in range(len(player_obj)):
            state = {
                'agent': {
                    'health': state_obj[i]['health'],
                    'weapon_name': state_obj[i]['weapon_name'],
                    'weapon_damage_n': state_obj[i]['weapon_damage_n'],
                    'weapon_damage_d': state_obj[i]['weapon_damage_d'],
                },
                'view': w.get_local(state_obj[i]['x'], state_obj[i]['y'],
                                    state_obj[i]['visibility']),
            }
            
            action = player_obj[i].update(state)
            action_obj.append((i, action, state_obj[i]['initiative']))
            if VERBOSE:
                print('\tplayer {0} ({1}): {2}'.format(
                        i, str(player_obj[i]), action))

        # first we need to process actions
        #   for example, attack another player based on their position
        # once that's done, we make appropriate changes to the state
        state_change_obj = []
        for i in range(len(player_obj)):
            state_change_obj.append({})

        random.shuffle(action_obj) # TODO consider initiative
        for action in action_obj:
            p = action[0]
            a = action[1].split(' ')

            if a[0] not in AGENT_COMMANDS:
                print('WARNING: {0}'.format(action))
                continue

            if a[0] == 'pass':
                pass
            elif a[0] == 'north':
                if w.is_empty(state_obj[p]['x'], state_obj[p]['y'] - 1):
                    state_change_obj[p]['y'] = state_obj[p]['y'] - 1
            elif a[0] == 'south':
                if w.is_empty(state_obj[p]['x'], state_obj[p]['y'] + 1):
                    state_change_obj[p]['y'] = state_obj[p]['y'] + 1
            elif a[0] == 'east':
                if w.is_empty(state_obj[p]['x'] + 1, state_obj[p]['y']):
                    state_change_obj[p]['x'] = state_obj[p]['x'] + 1
            elif a[0] == 'west':
                if w.is_empty(state_obj[p]['x'] - 1, state_obj[p]['y']):
                    state_change_obj[p]['x'] = state_obj[p]['x'] - 1
            #print(action)

        for i in range(len(player_obj)):
            for k in state_change_obj[i].keys():
                state_obj[i][k] = state_change_obj[i][k]

        cycles_left -= 1
        if cycles_left <= 0:
            done = True



class AbstractAgent():
    def __str__(self):
        return 'AbstractAgent'
    def update(self, state):
        return ('pass')

class PassAgent(AbstractAgent):
    def __str__(self):
        return 'PassAgent'
    def update(self, state):
        #print(state)
        return ('pass')

class StumbleAgent(AbstractAgent):
    def __str__(self):
        return 'StumbleAgent'
    def update(self, state):
        print(state['view'])
        actions = ['north', 'south', 'east', 'west']
        return random.choice(actions)

if __name__ == "__main__":
    main()
