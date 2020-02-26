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
    "items",
]
API_KEY = os.getenv("API_KEY")
headers = {"Authorization": f"Token {API_KEY}"}


def game_init(**kwargs):
    response = requests.get(url=base_url + "/init", headers=headers).json()

    if all([key in response for key in expected_room_response]):
        return response
    else:
        print(response)
        raise Exception(response)


# direction, room_id=None
def explore_room(**payload):
    required = ["direction", "room_id"]

    if not all([key in required for key in payload]):
        print(payload)
        raise

    data = {"direction": payload["direction"]}
    if payload["room_id"] is not None and payload["room_id"] != "?":
        payload["next_room_id"] = str(payload["room_id"])

    try:
        data_payload = json.dumps(data)

        response = requests.post(
            url=base_url + "/move", headers=headers, data=data_payload
        ).json()

        if all([key in response for key in expected_room_response]):
            return response
        else:
            print(response)
            raise Exception(response)
    except Exception:
        raise


# item_name
def pick_item(**payload):
    if "name" not in payload:
        raise
    data = {"name": payload["name"]}
    try:
        data_payload = json.dumps(data)

        response = requests.post(
            url=base_url + "/take", headers=headers, data=data_payload
        ).json()
        return response
    except Exception:
        raise


# name
def examine(**payload):
    if "name" not in payload:
        raise
    data = {"name": payload["name"]}

    try:
        data_payload = json.dumps(data)

        response = requests.post(
            url=base_url + "/examine", headers=headers, data=data_payload
        ).json()
        return response
    except Exception:
        raise


def check_status(**payload):
    try:
        response = requests.post(url=base_url + "/status", headers=headers).json()
        return response
    except Exception:
        raise
