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

graph = {}

curr_directions = []

while len(graph) != len(world.rooms):
    
    c_room = player.current_room

    exits = c_room.get_exits()

    graph[c_room.id] = {}
    
    for e in exits:
        room = c_room.get_room_in_direction(e)
        graph[c_room.id][e] = room.id

    print("graph: ", graph, "\ncurr: ", c_room.id, "\ndir: ", 'blank')

    if 'n' in exits and c_room.get_room_in_direction('n').id not in graph:
        curr_directions.append('n')
        traversal_path.append('n')
        player.travel('n')
        print("1graph: ", graph, "\ncurr: ", c_room.id, "\ndir: ", 'n')
    
    elif 's' in exits and c_room.get_room_in_direction('s').id not in graph:
        curr_directions.append('s')
        traversal_path.append('s')
        player.travel('n')
        print("2graph: ", graph, "\ncurr: ", c_room.id, "\ndir: ", 's')

    elif 'e' in exits and c_room.get_room_in_direction('e').id not in graph:
        curr_directions.append('e')
        traversal_path.append('e')
        player.travel('e')
        print("3graph: ", graph, "\ncurr: ", c_room.id, "\ndir: ", 'e')

    elif 'w' in exits and c_room.get_room_in_direction('w').id not in graph:
        curr_directions.append('w')
        traversal_path.append('w')
        player.travel('w')
        print("4graph: ", graph, "\ncurr: ", c_room.id, "\ndir: ", 'w')

    else:
        last_dir = curr_directions.pop()
        r = reverse_dir[last_dir]

        traversal_path.append(r)
        player.travel(r)

        print("5graph: ", graph, "\ncurr: ", c_room.id, "\ndir: ", r)
    
    
    # neighbors = [c_room.get_room_in_direction(e) for e in exits]

    # if c_room.id not in graph:
    #     graph[c_room.id] = {}

    #     for e in exits:
    #         room = c_room.get_room_in_direction(e)
    #         graph[c_room.id][e] = room.id

    # for n in neighbors:
    #     if n.id not in graph:




    #         graph[c_room.id][e] = room.id

    #     d = random.choice(exits)

    #     player.travel(d)
    #     traversal_path.append(d)
    #     curr_directions.append(d)

    # else:







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
