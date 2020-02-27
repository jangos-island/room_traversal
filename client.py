from datetime import datetime
import json

from player import Player
from room import Room
from apis import game_init
from utils import debounce, record_move, traverse


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

    print(f"Please choose running mode:")
    print(f"1 - automatic traversal")
    print(f"2 - manual")

    running_mode = int(input())

    if running_mode == 1:
        traverse(rooms, player, game_state)
    elif running_mode == 2:
        print(f"manual mode")
