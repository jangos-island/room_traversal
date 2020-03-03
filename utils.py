import requests
import random
import json
from datetime import datetime
from collections import deque

from os import system, name 
from room import Room
from apis import explore_room, pick_item, check_status, examine, sell_item, get_last_proof, submit_proof, changeName, confirmName, get_balance
from time import sleep
from miner import proof_of_work

def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

reverse_direction = {"n": "s", "s": "n", "w": "e", "e": "w"}

notable_rooms = {
    "shop": 1,
    "winged_shrine": 22,
    "wishing_well": 55,
    "pirate_ry": 467,
    "linhs_shrine": 461,
    "recall_room": 492,
    "glasowyns_grave": 499,
    "fully_shrine": 374,
    "aaron": 486,
    "the_transmogriphier" : 495,
    "mining_room": 3
}


def get_closest_path(rooms, current_room, to_room_id):
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
        if current["direction"][1] == to_room_id:
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


def record_move(rooms, to_room, from_room=None, direction=None):
    if to_room.id not in rooms:
        new_room = {
            "directions": {"n": None, "s": None, "w": None, "e": None},
            "room": to_room.get_json(),
        }
        for exit in to_room.exits:
            new_room["directions"][exit] = "?"
        rooms[to_room.id] = new_room
    
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
        sleep(delay)

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

def repl(rooms, player, game_state):
    clear()
    while True:
        choice = None
        while choice is None:
            try:
                choice = int(input("type in your choice (0 for list of command): "))
            except Exception:
                print('Invalid input')

        if choice == 0:
            print_commands()
        elif choice == 1:
            print(player.current_room)
        elif choice == 2:
            for room, id in notable_rooms.items():
                path = get_closest_path(rooms, player.current_room, id)
                print(f"{room}: {len(path)} rooms away")
        elif choice == 31:
            travel(rooms, player, game_state, "n")
        elif choice == 32:
            travel(rooms, player, game_state, "s")
        elif choice == 33:
            travel(rooms, player, game_state, "w")
        elif choice == 34:
            travel(rooms, player, game_state, "e")
        elif choice == 41:
            directions = get_closest_path(rooms, player.current_room, notable_rooms["aaron"])
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


def travel(rooms, player, game_state, direction):
    response = debounce(
        explore_room,
        game_state,
        {"direction": direction, "room_id": rooms[player.current_room.id]["directions"][direction]},
    )
    room = Room(response)
    print(f"Current room: {room}")

    items = []
    if "items" in response:
        items = response["items"]
    if len(items) > 0:
        print(items)

    player.travel(room)

def print_commands():
    print(f"0 - command")
    print()

    print(f"1 - print current room")
    print(f"12 - print items in current room")
    print(f"13 - check status")
    print(f"14 - examine")
    print()

    print(f"2 - print distance to notable rooms")
    print(f"21 - go to notable rooms")
    print()

    print(f"31 - travel north")
    print(f"32 - travel south")
    print(f"33 - travel west")
    print(f"34 - travel east")
    print()

    print(f"41 - travel to winged shrine")

    print(f"5 - quit")


def work(rooms, player, game_state):
    response = debounce(check_status, game_state)
    my_items = []
    if "inventory" in response:
        my_items = response["inventory"]

    while True:
        directions = get_closest_path(rooms, player.current_room, random.randint(1,499))
        if len(directions) == 0:
            break

        print(f"\n*** Room count: {len(rooms)}")
        print(f"Path length: {len(directions)}")

        for direction in directions:
            if len(my_items) < 10:
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

                if "items" in response and len(response["items"]) > 0:
                    for item in response["items"]:
                        debounce(pick_item, game_state, {"name": item})
                        my_items.append(item)
                        print(my_items)
            else:
                print(my_items)
                directions = get_closest_path(rooms, player.current_room, notable_rooms["shop"])
                path_count_to_shop = len(directions)
                for direction in directions:
                    current_room = player.current_room
                    response = debounce(
                        explore_room,
                        game_state,
                        {"direction": direction[0], "room_id": direction[1]},
                    )

                    room = Room(response)
                    print(f"{path_count_to_shop} to shop - Current room: {room}")
                    path_count_to_shop -= 1
                    player.travel(room)
        
                for item in my_items:
                    debounce(sell_item, game_state, {"name": item})
                    debounce(sell_item, game_state, {"name": item, "confirm": "yes"})

                response = debounce(check_status, game_state)
                print()
                print(json.dumps(response, indent=4))
                my_items = []
                if "inventory" in response:
                    my_items = response["inventory"]
                
                should_continue = input("do you want to collect more items? [y/n]  ")

                if should_continue == "y":
                    break
                else:
                    return


def travel_to_room(rooms, player, game_state, roomId):
    directions = get_closest_path(rooms, player.current_room, roomId)
    path_count = len(directions)
    for direction in directions:
        current_room = player.current_room
        response = debounce(
            explore_room,
            game_state,
            {"direction": direction[0], "room_id": direction[1]},
        )

        room = Room(response)
        print(f"\n{path_count} rooms away to destination room. Currently in: {room}")
        path_count -= 1
        player.travel(room)

def mine(rooms, player, game_state):
    while True:
        print(f"\nTravel to the wishing well...")
        travel_to_room(rooms, player, game_state, notable_rooms["wishing_well"])
        response = debounce(examine, game_state, {"name": "WELL"})

        message = response["description"]
        room_number = int(message[message.rfind(' ') + 1:])
        
        print(f"\nThe next room to mine: {room_number}\n")
        travel_to_room(rooms, player, game_state, room_number)

        has_mine = False
        while not has_mine:
            # work for a proof
            last_proof = debounce(get_last_proof, game_state)
            new_proof = proof_of_work(last_proof)

            # mine a coin 
            print(f"Submitting proof: {new_proof}")
            response = debounce(submit_proof, game_state, {"proof": new_proof})
            print(json.dumps(response, indent=2))

            if "messages" in response:
                has_mine = "New Block Forged" in response["messages"]

                if has_mine:
                    response = debounce(get_balance, game_state)
                    print('\n\n Balance:')
                    print(json.dumps(response, indent=2))


def change_name(rooms, player, game_state):
    travel_to_room(rooms, player, game_state, notable_rooms["pirate_ry"])
    name = input("Type in Your Name :")

    response = debounce(changeName, game_state, {"name": name})
    response = debounce(confirmName, game_state, {"name": name})
    print(json.dumps(response, indent=2))