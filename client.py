import requests
import random
from datetime import datetime
import time

from player import Player
from room import Room
from apis import game_init, explore_new_room

reverse_direction = {"n": "s", "s": "n", "w": "e", "e": "w"}


def record_move(rooms, to_room, from_room=None, direction=None):
    if to_room.id not in rooms:
        new_room = {
            "directions": {"n": None, "s": None, "w": None, "e": None},
            "room": to_room,
        }
        for exit in to_room.exits:
            new_room["directions"][exit] = "?"
        rooms[to_room.id] = new_room
    if from_room is not None:
        rooms[from_room.id]["directions"][direction] = to_room.id
        rooms[to_room.id]["directions"][reverse_direction[direction]] = from_room.id


def get_directions_to_unseen_room(rooms, current_room):
    seen = set([current_room.id])
    exits = [
        {"direction": exit, "path": []}
        for exit in rooms[current_room.id]["directions"].items()
        if exit[1] is not None and exit[1] not in seen
    ]

    random.seed(random.randint(0, 100))
    random.shuffle(exits)

    while len(exits) > 0:
        current = exits.pop()
        if current["direction"][1] == "?":
            current["path"].append(current["direction"])
            return current["path"]
        else:
            seen.add(current["direction"][1])
            next_exits = [
                {"direction": exit, "path": current["path"] + [current["direction"]]}
                for exit in rooms[current["direction"][1]]["directions"].items()
                if exit[1] is not None and exit[1] not in seen
            ]
            random.seed(0, 100)
            random.shuffle(next_exits)
            exits = exits + next_exits


def traverse(rooms, player, game_state):

    while len(rooms.keys()) != 500:
        directions = get_directions_to_unseen_room(rooms, player.current_room)

        for direction in directions:
            print(f"Room count: {len(rooms)}")
            time_now = datetime.now()
            elapsed_time = time_now - game_state["last_call"]
            cooldown = max(15, game_state["cooldown"])

            if elapsed_time.seconds < cooldown:
                delay = cooldown - elapsed_time.seconds
                time.sleep(delay)

            current_room = player.current_room
            response = explore_new_room(direction[0], direction[1])
            game_state["last_call"] = datetime.now()
            game_state["cooldown"] = response["cooldown"]
            game_state["errors"] = response["errors"]
            game_state["messages"] = response["messages"]

            room = Room(response)
            print(f"Current room: {room}")
            player.travel(room)
            record_move(rooms, room, current_room, direction[0])

            print(game_state)
            print("------\n")


if __name__ == "__main__":
    # Create a player with token
    player = Player()

    # Game State
    # TODO: persist game state in a text file and load upon init
    game_state = {"last_call": None, "cooldown": None, "errors": None, "messages": None}

    # Rooms
    # TODO: persist room in a text file and load rooms from it
    rooms = {}

    if len(rooms.keys()) == 0:

        # Test API - initialize room
        response = game_init()
        game_state["last_call"] = datetime.now()
        game_state["cooldown"] = response["cooldown"]
        game_state["errors"] = response["errors"]
        game_state["messages"] = response["messages"]

        room = Room(response)
        print(room)
        player.play(room)
        record_move(rooms, room)

    print(f"Please choose running mode:")
    print(f"1 - automatic traversal")
    print(f"2 - manual")

    running_mode = int(input())

    if running_mode == 1:
        traverse(rooms, player, game_state)
    elif running_mode == 2:
        print(f"manual mode")
