from datetime import datetime
import time


def debounce(callback, game_state, params={}):
    time_now = datetime.now()
    elapsed_time = time_now - game_state["last_call"]
    cooldown = max(15, game_state["cooldown"])

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
