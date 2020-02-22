from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

directions = ["n", "s", "e", "w"]

reverse_dir = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

graph = {} #visited

unexplored = set() #found but not visited, edges

c_room = player.current_room

exits = c_room.get_exits()

d = random.choice(exits)
r = reverse_dir[d]


if c_room.id not in graph:
    graph[c_room.id] = {k:'?' for k in exits}


for e in exits:
    room = c_room.get_room_in_direction(e)
    unexplored.add(room)


while len(unexplored) != 0:

    c_room = player.current_room
    
    if '?' in graph[c_room.id].values():
        if 'n' in graph[c_room.id] and graph[c_room.id]['n'] == '?':
            d = 'n'
        if 's' in graph[c_room.id] and graph[c_room.id]['s'] == '?':
            d = 's'
        if 'e' in graph[c_room.id] and graph[c_room.id]['e'] == '?':
            d = 'e'
        if 'w' in graph[c_room.id] and graph[c_room.id]['w'] == '?':
            d = 'w'

        player.travel(d)
        room = player.current_room
        unexplored.remove(room)
        traversal_path.append(d)

        if room.id not in graph:
            graph[room.id] = {k:'?' for k in room.get_exits()}

        graph[c_room.id][d] = room.id
        graph[room.id][r] = c_room.id

        for k, v in graph[room.id].items():
            if v == '?':
                unexplored.add(room.get_room_in_direction(k))

    else:
        q = Queue()
        # explored = set()

        # q.enqueue(c_room)


        
        for e, r in graph[c_room.id].items():
            q.enqueue([[e,r]])

        while q.size() != 0:
            path = q.dequeue()
            vert = path[-1]

            if '?' in graph[vert[1]].values():
                for e, r in path:
                    player.travel(e)
                    traversal_path.append(e)
                break

            else:
                for e, r in graph[vert[1]].items():
                    if r != c_room.id and r not in [room for ex, room in path]:
                        q.enqueue(list(path) + [[e, r]])
            print('graph: ', graph, "\n c: ", c_room.id,"\n un: ", unexplored)




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
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
