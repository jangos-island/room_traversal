from datetime import datetime
import json

from player import Player
from room import Room
from apis import game_init
from utils import debounce, record_move, traverse, repl, work, mine, change_name


if __name__ == "__main__":
    player = Player()

    # Game State
    game_state = {
        "last_call": datetime.now(),
        "cooldown": 15,
        "errors": None,
        "messages": None,
    }

    # Load Rooms
    loaded_rooms = None
    with open("room.txt") as json_file:
        loaded_rooms = json.load(json_file)
    
    rooms = {}
    for key, room in loaded_rooms.items():
        rooms[int(key)] = room

    if len(rooms.keys()) != 0:
        print(f"There are already {len(rooms)} visited rooms")
        
    # Initialize the Game
    response = debounce(game_init, game_state)

    room = Room(response)
    print(f"Current room: {room}")
    player.play(room)
    record_move(rooms, room)

    # Game Mode
    print(f"Please choose running mode:")
    print(f"1 - automatic traversal")
    print(f"2 - manual")
    print(f"3 - work to find and sell items")
    print(f"4 - mine for coins")
    print(f"5 - change name")
    running_mode = int(input())

    if running_mode == 1:
        traverse(rooms, player, game_state)
    elif running_mode == 2:
        repl(rooms, player, game_state)
    elif running_mode == 3:
        work(rooms, player, game_state)
    elif running_mode == 4:
        mine(rooms, player, game_state)
    elif running_mode == 5:
        change_name(rooms, player, game_state)
