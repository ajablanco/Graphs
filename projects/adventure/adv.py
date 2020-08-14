from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']



# Before we proceed:

# a. have a traversal graph(an actual graph or just a normal dictionary) that
# has the starting room as key. the value will be a dictionary with directions as keys
# and "?" as value

#     eg: tg = {0: {n: "?", s: "?", e: "?", w:"?"}}

#     - do not hardcode this
#     - you can get 0 from one of the attributes in player class
#     - you can do a dictionary comprehension to generate the 'n: "?"...' part using the
#     list of exits available for that room

traversal_graph = {player.current_room.id: {direction:"?" for direction in player.current_room.get_exits()}}
print(player.current_room.get_exits())
print("lala", traversal_graph)

# b. opposite_dir(either a dictionary or an attribute in your graph class)
#     - key will be direction and value will be opposite of the key
opposite_dir = {"n": "s", "s": "n", "w": "e", "e": "w"}

# c. traversal_path which will contain all the directions you traverse
traversal_path = []

# 1.  Function to get available exits(directions in traversal_graph that has "?" as value)
#     for current room

#     - this function accepts a room as argument
#     - declare an empty list which will contain the directions that are still available for the given room
#     - loop through the dictionary of available exits ({n: "?", s: "?", e: "?", w:"?"})
#       - if the direction has a value of "?", append it to the list
#     - return the list

#     Notes

#     - this function will return an empty list if you are on a dead end

def get_available_exits(room):
    still_available = []

    for d in traversal_graph[room]:
        if traversal_graph[room][d] == "?":
            still_available.append(d)

    return still_available



# 2.  Function to traverse list until you reach a dead end(room with no available exits) -> DFT

#     - this will take a room as an argument
def dft(room):
#     - we'll set up a while loop with the condition that as long as there are AVAILABLE EXITS in the current room, we'll continue running the code inside this loop
    while len(get_available_exits(room)) > 0:
#     - first, we randomly choose a direction from the LIST OF AVAILABLE EXITS
        rand_dir = random.choice(get_available_exits(room))
#     - we also want to store the current room we're in to a variable so we can reference later once we travel

        previous = player.current_room.id
        player.travel(rand_dir)
        current = player.current_room.id
#     - we can then append that direction to traversal_path
        traversal_path.append(rand_dir)
#     - at this point, we're on a different room, check if the room doesn't exist in your traversal graph

#       - if it doesn't, add it to your traversal graph
        if current not in traversal_graph:
            traversal_graph[current] = {d:"?" for d in player.current_room.get_exits()}
        traversal_graph[current][opposite_dir[rand_dir]] = previous

        traversal_graph[previous][rand_dir] = current
#     - outside of the if statement, add the previous room you're in as the value of the opposite direction that you traveled in your traversal graph

#     - lastly, you want to update the room to be the new room you're currently in

        room = current





# 3.  From dead end, this function returns the room(which will be used as target) - BFS Nearest room
def bfs(room):
    queue = [room]
    visited = set()

    while len(queue) > 0:
        r = queue.pop(0)
        if r not in visited:
            visited.add(r)
            if len(get_available_exits(r)) > 0:
                return r
            for room in list(traversal_graph[r].values()):
                queue.append(room)

def bft(target, room):
    queue = [[room]]
    visited = set()

    room_path = list()

    while len(queue) > 0:
        r = queue.pop(0)
        if r[-1] not in visited:
            visited.add(r[-1])
            if r[-1] == target:
                room_path = r
                break
            for room in list(traversal_graph[r[-1]].values()):
                copy_r = list(r) + [room]
                queue.append(copy_r)
    path = []
    for i in range(len(room_path)-1):
        for d in traversal_graph[room_path[i]]:
            if traversal_graph[room_path[i]][d] == room_path[i+1]:
                path.append(d)
    return path

while len(traversal_graph) != len(world.rooms):
    dft(player.current_room.id)

    target_room = bfs(player.current_room.id)

    path = bft(target_room, player.current_room.id)

    for d in path:
        player.travel(d)
        traversal_path.append(d)

                


#     - this function takes in a room as an argument
#     - we create a queue and add the room to it and also set up your visited set
#     - declare a variable and initialize it as None or 0
#     - do a bft traversal

#       - after adding the room to your set, have an if statement to check if the length of AVAILABLE EXITS for that room is greater than 0

#         - if it is, that's your target room and set the value of the variable you declared eaelier as that room and return it

#       - loop through the current room's available exits and append the ROOM(not the direction) to your queue

# 4) Still on dead end, this function will return a list containing all the directions
#    to travel in order to get to target room - BFT PATH

#    - this function takes in a TARGET ROOM and a starting room, which is the current room you're in, as arguments
#    - we create a queue, but this time, instead of adding just the room, we're going to add an array containing the starting room
#    - we also create a visited set
#    - and a final_path which will contain all the directions
#    - same thing as normal BFS
#      - after you've added the room to your visited set, check have an if statement checking if the room[-1](since room is actually an array and we only want the last element there) is the same as TARGET ROOM, assign room(which is the path or a list) as the new value of final_path and "break" out of the while loop
#      - else:
#        - do the loop
#        - if you use traversal_graph[room] in your for loop, this will give you the keys, which are directions and we don't want that
#        - instead, we want to use list(traversal_graph[room].values())
#        - we create a copy of room and add the neighbor rooms just like in BFS in your assignment


#     - AFTER THE WHILE LOOP EXECUTES
#     - your final path should now have the rooms path which should look something like this

#             eg: if you use this map "maps/test_loop_fork.txt" and you're in room 17 if 1 has north and east unexplored

#                 [17, 16, 15, 1]

#     - now we declare a new path list which will contain the directions that we'll need to traverse to get to our target room
#     - for loop using the length of final_path
#         - inside this for loop, we'll have another for loop looping over traversal_graph[final_path[i]]
#             - this for loop will loop over the directions available to that room
#             - have an if statement checking if the traversal_graph[final_path[i]][direction] is the same as final_path[i + 1]
#                 - so for [17, 16, 15, 1], in your traversal_graph, 17: {s: "16"}
#                 - so for room 17, traversal_graph[final_path[i]][direction] is equal to 16
#                 - if it is, we append it new path list we created


#     - after your for loop, return the path

# 5. we create a while loop that will finally complete this damn thing


#     - the condition is that as long as the length of your traversal graph is not equal to the number of rooms in your map, continue to do these stuff
#     - we use DFT function passing in the player's current room id
#     - grab the nearest room using your BFS Nearest Room function
#     - grab the path to nearest using your BFT PATH function
#     - loop over the result of BFT PATH
#         - travel to each direction
#         - append each direction to your traversal path


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
