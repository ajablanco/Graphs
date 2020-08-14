from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

world = World()

player = Player(world.starting_room)

print({direction for direction in player.current_room.get_exits()})


