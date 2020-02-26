import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
expected_room_response = [
    "room_id",
    "title",
    "description",
    "coordinates",
    "elevation",
    "terrain",
    "exits",
    "cooldown",
    "errors",
    "messages",
]
API_KEY = os.getenv("API_KEY")
headers = {"Authorization": f"Token {API_KEY}"}


def game_init():
    response = requests.get(url=base_url + "/init", headers=headers).json()

    if all([key in response for key in expected_room_response]):
        return response
    else:
        print(response)
        raise Exception(response)


def explore_new_room(direction, room_id=None):
    payload = {"direction": direction}
    if room_id is not None and room_id != "?":
        payload["next_room_id"] = str(room_id)
    json_payload = json.dumps(payload)

    response = requests.post(
        url=base_url + "/move", headers=headers, data=json_payload
    ).json()
    if all([key in response for key in expected_room_response]):
        return response
    else:
        print(response)
        raise Exception(response)
