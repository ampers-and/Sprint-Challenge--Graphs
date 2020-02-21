from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
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

graph = {}

visited = set()

reverse_dir = {"n": "s", "s": "n", "e": "w", "w": "e"}

c_dir = []


def traverse1():
    global player
    global traversal_path
    global graph
    global visited
    global reverse_dir
    global c_dir

    c_room = player.current_room
    exits = c_room.get_exits()
    visited.add(c_room)

    if c_room.id not in graph:
        graph[c_room.id] = {}

    for e in exits:

        room = c_room.get_room_in_direction(e)
        graph[c_room.id][e] = room.id

        # if room not in visited:
        #     player.travel(e)
        #     traversal_path.append(e)
        #     traverse()
        # else:
        #     player.travel(reverse_dir[e])
        # if len(visited) == len(world.rooms):
        #     return

        if room not in visited:
            player.travel(e)
            traversal_path.append(e)
            c_dir.append(e)
            traverse1()

        else:
            last_dir = c_dir.pop()
            new_dir = reverse_dir[last_dir]
            traversal_path.append(new_dir)
            player.travel(new_dir)


def traverse2():
    while len(visited) < len(world.rooms):

        c_room = player.current_room
        exits = c_room.get_exits()
        visited.append(c_room)
        c_directions = []

        if c_room.id not in graph:
            graph[c_room.id] = {}

            for e in exits:
                room = c_room.get_room_in_direction(e)

                graph[c_room.id][e] = room.id

                if room not in visited:
                    player.travel(e)
                    traversal_path.append(e)
                    c_directions.append(e)
                else:
                    pass


def traverse():
    global player
    global traversal_path
    global graph
    global visited
    global reverse_dir
    global c_dir
    print("player room", player.current_room.id)

    while len(visited) != len(world.rooms):
        c_room = player.current_room
        print("player", player)
        print("room", player.current_room.id)
        exits = c_room.get_exits()
        print("exits", exits)

        visited.add(c_room)

        if (
            "n" in exits
            and c_room.get_room_in_direction("n") is not None
            and c_room.get_room_in_direction("n") not in visited
        ):
            c_dir.append("n")
            traversal_path.append("n")
            player.current_room = player.travel("n")
            print("room", player.current_room.id)

        elif (
            "s" in exits
            and c_room.get_room_in_direction("s") is not None
            and c_room.get_room_in_direction("s") not in visited
        ):
            c_dir.append("s")
            traversal_path.append("s")
            player.current_room = player.travel("s")
            print("room", player.current_room.id)

        elif (
            "e" in exits
            and c_room.get_room_in_direction("e") is not None
            and c_room.get_room_in_direction("e") not in visited
        ):
            c_dir.append("e")
            traversal_path.append("e")
            player.current_room = player.travel("e")
            print("room", player.current_room.id)

        elif (
            "w" in exits
            and c_room.get_room_in_direction("w") is not None
            and c_room.get_room_in_direction("w") not in visited
        ):
            c_dir.append("w")
            traversal_path.append("w")
            player.current_room = player.travel("w")
            print("room", player.current_room.id)

        else:
            last_dir = c_dir.pop()
            new_dir = reverse_dir[last_dir]
            traversal_path.append(new_dir)
            player.current_room = player.travel(new_dir)
            print("room", player.current_room.id)


def traverse3():
    global player
    global traversal_path
    global graph
    global visited
    global reverse_dir
    global c_dir

    c_room = player.current_room
    exits = c_room.get_exits()
    visited.add(c_room)

    if c_room.id not in graph:
        graph[c_room.id] = {}

    while len(exits) > 0:
        e = exits.pop()

        room = c_room.get_room_in_direction(e)
        graph[c_room.id][e] = room.id

        # if room not in visited:
        #     player.travel(e)
        #     traversal_path.append(e)
        #     traverse()
        # else:
        #     player.travel(reverse_dir[e])
        # if len(visited) == len(world.rooms):
        #     return

        if room not in visited:
            player.travel(e)
            traversal_path.append(e)
            c_dir.append(e)
            traverse3()

        else:
            last_dir = c_dir.pop()
            new_dir = reverse_dir[last_dir]
            traversal_path.append(new_dir)
            player.travel(new_dir)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


def traverse4():
    global player
    global traversal_path
    global graph
    global visited

    c_room = player.current_room

    s = Stack()
    s.push(c_room)
    while s.size() != 0:
        c = s.pop()
        while len(c_dir) > 0:
            l_dir = c_dir.pop()
            new_dir = reverse_dir[l_dir]
            traversal_path.append(new_dir)
        if c not in visited:
            visited.add(c)
            exits = c.get_exits()
            for e in exits:
                traversal_path.append(e)
                room = c.get_room_in_direction(e)
                s.push(room)
                c_dir.append(e)


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def traverse5():
    global player
    global traversal_path
    global graph
    global visited
    global c_dir

    c_room = player.current_room

    q = Queue()
    q.enqueue(c_room)
    while q.size() != 0:
        c = q.dequeue()

        if c not in visited:
            visited.add(c)

        exits = c.get_exits()
        for e in exits:
            room = c.get_room_in_direction(e)

            if room not in visited:
                traversal_path.append(e)
                visited.add(room)
                q.enqueue(room)
                c_dir.append(e)
            else:
                while len(c_dir) > 0:
                    l_dir = c_dir.pop()
                    new_dir = reverse_dir[l_dir]
                    traversal_path.append(new_dir)


def traverse6():
    global player
    global traversal_path
    global graph
    global visited

    c_room = player.current_room

    visited.add(c_room)

    exits = c_room.get_exits()

    for e in exits:
        room = c_room.get_room_in_direction(e)

        if room not in visited:
            traversal_path.append(e)
            player.travel(e)
            traverse6()
        else:
            pass


traverse4()
print("graph", graph)
print("path", traversal_path)


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
