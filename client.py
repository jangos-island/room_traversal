import requests
import random
from datetime import datetime
import json

from player import Player
from room import Room
from apis import game_init, explore_room, pick_item, check_status, examine
from utils import debounce

reverse_direction = {"n": "s", "s": "n", "w": "e", "e": "w"}


def record_move(rooms, to_room, from_room=None, direction=None):
    if to_room.id not in rooms:
        new_room = {
            "directions": {"n": None, "s": None, "w": None, "e": None},
            "room": to_room.get_json(),
        }
        for exit in to_room.exits:
            new_room["directions"][exit] = "?"
        rooms[to_room.id] = new_room
        
        if from_room is not None:
            rooms[from_room.id]["directions"][direction] = to_room.id
            rooms[to_room.id]["directions"][reverse_direction[direction]] = from_room.id

        with open('room.txt', 'w') as outfile:
            json.dump(rooms, outfile, sort_keys=True)
        

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
            print(current["path"])
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

            current_room = player.current_room
            response = debounce(
                explore_room,
                game_state,
                {"direction": direction[0], "room_id": direction[1]},
            )

            room = Room(response)
            print(f"Current room: {room}")
            player.travel(room)
            record_move(rooms, room, current_room, direction[0])

            # check for items
            # for item in response["items"]:
            #     print("item: ", item)
            #     response = debounce(examine, game_state, {"name": item})
            #     response = debounce(pick_item, game_state, {"name": item})
            #     response = debounce(check_status, game_state)

            # print(game_state)
            # print("------\n")


if __name__ == "__main__":
    # Create a player with token
    player = Player()

    # Game State
    # TODO: persist game state in a text file and load upon init
    game_state = {
        "last_call": datetime.now(),
        "cooldown": 15,
        "errors": None,
        "messages": None,
    }

    # Rooms
    loaded_rooms = None
    with open("room.txt") as json_file:
        loaded_rooms = json.load(json_file)
    
    rooms = {}
    for key, room in loaded_rooms.items():
        rooms[int(key)] = room

    if len(rooms.keys()) != 0:
        print(f"There are already {len(rooms)} visited rooms")
        
    # Test API - initialize room
    response = debounce(game_init, game_state)

    room = Room(response)
    print(f"Current room: {room}")
    player.play(room)
    record_move(rooms, room)

    # check for items
    # for item in response["items"]:
    #     print("item: ", item)
    #     response = debounce(examine, game_state, {"name": item})
    #     response = debounce(pick_item, game_state, {"name": item})
    #     response = debounce(check_status, game_state)

    print(f"Please choose running mode:")
    print(f"1 - automatic traversal")
    print(f"2 - manual")

    running_mode = int(input())

    if running_mode == 1:
        traverse(rooms, player, game_state)
    elif running_mode == 2:
        print(f"manual mode")
