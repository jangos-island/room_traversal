import requests
import random
import time
import json
from datetime import datetime
from collections import deque

from room import Room
from apis import explore_room, pick_item, check_status, examine

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
        
        # if from_room is not None:
        #     rooms[from_room.id]["directions"][direction] = to_room.id
        #     rooms[to_room.id]["directions"][reverse_direction[direction]] = from_room.id

        # with open('room.txt', 'w') as outfile:
        #     json.dump(rooms, outfile, sort_keys=True, indent=2)
    
    if from_room is not None and rooms[from_room.id]["directions"][direction] == '?':
        rooms[from_room.id]["directions"][direction] = to_room.id
        rooms[to_room.id]["directions"][reverse_direction[direction]] = from_room.id

        with open('room.txt', 'w') as outfile:
            json.dump(rooms, outfile, sort_keys=True, indent=2)
        

def get_directions_to_unseen_room(rooms, current_room):
    seen = set([current_room.id])
    exits_list = [
        {"direction": exit, "path": []}
        for exit in rooms[current_room.id]["directions"].items()
        if exit[1] is not None and exit[1] not in seen
    ]

    random.seed(random.randint(0, 100))
    random.shuffle(exits_list)

    exits = deque(exits_list)

    while len(exits) > 0:
        current = exits.popleft()
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
            exits.extend(next_exits)
    return []


def traverse(rooms, player, game_state):

    while True:
        directions = get_directions_to_unseen_room(rooms, player.current_room)
        if len(directions) == 0:
            break
        
        print(f"\n*** Room count: {len(rooms)}")
        print(f"Path length: {len(directions)}")
        path_count = len(directions)

        for direction in directions:
            current_room = player.current_room
            response = debounce(
                explore_room,
                game_state,
                {"direction": direction[0], "room_id": direction[1]},
            )

            room = Room(response)
            print(f"{path_count} - Current room: {room}")
            path_count -= 1
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


def debounce(callback, game_state, params={}):
    time_now = datetime.now()
    elapsed_time = time_now - game_state["last_call"]
    cooldown = game_state["cooldown"]

    if elapsed_time.seconds < cooldown:
        delay = cooldown - elapsed_time.seconds
        time.sleep(delay)

    response = callback(**params)

    game_state["last_call"] = datetime.now()
    if "cooldown" in response:
        game_state["cooldown"] = response["cooldown"]
    if "erros" in response:
        game_state["erros"] = response["erros"]
    if "messages" in response:
        game_state["messages"] = response["messages"]
    print(game_state)

    return response
