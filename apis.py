import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
mine_url = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
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
        data["next_room_id"] = str(payload["room_id"])

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

#status/inventory
def check_status(**payload):
    try:
        response = requests.post(url=base_url + "/status", headers=headers).json()
        return response
    except Exception:
        raise

def pray(**payload):
    try:
        response = requests.post(url=base_url + "/pray", headers=headers).json()
        return response
    except Exception:
        raise

def warp(**payload):
    if "bodywear" and "footwear" not in payload:
        raise
    data = {"name": payload["bodywear"]}
    data = {"name": payload["footwear"]}

    try:
        data_payload = json.dumps(data)

        response = requests.post(
            url=base_url + "/warp", headers=headers, data=data_payload
        ).json()
        return response
    except Exception:
        raise

#wear item
def equipItem(equipItem):
    if "name" and "bodywear" and "footwear" not in payload:
        raise
    data = {"name":f"{equipItem}"}
    data = {"name": payload["bodywear"]}
    data = {"name": payload["footwear"]}

    try:
        data_payload = json.dumps(data)
        response = requests.post(url = base_url + "/wear", headers = headers).json()
        return data
    except Exception:
        raise

#remove item
def unequipItem(unequipItem):
    data = {"name":f"{unequipItem}"}
    response = requests.post(url = base_url + "/undress", headers = headers).json()
    return data    
#change name
def changeName(**payload):
    if "name" not in payload:
        print("invalid name")
        return    
    data = {"name": payload["name"]}

    try:
        data_json = json.dumps(data)
        response = requests.post(url = base_url + "/change_name", headers = headers, data=data_json).json()
        return response
    except Exception:
        raise

def confirmName(**payload):
    if "name" not in payload:
        print("invalid name")
        return    
    data = {"name": payload["name"], "confirm": "aye"}

    try:
        data_json = json.dumps(data)
        response = requests.post(url = base_url + "/change_name", headers = headers, data=data_json).json()
        return response
    except Exception:
        raise

def sell_item(**payload):
    if "name" not in payload:
        return
    data = {
        "name": payload["name"]
    }
    if "confirm" in payload:
        data["confirm"] = payload["confirm"]
    
    try:
        data_json = json.dumps(data)
        response = requests.post(
            url=base_url + "/sell", headers=headers, data=data_json
        ).json()
        return response
    except Exception:
        raise


def get_last_proof(**payload):
    try:
        response = requests.get(url=mine_url + "/last_proof", headers=headers).json()
        return response
    except Exception:
        raise

def submit_proof(**payload):
    if "proof" not in payload:
        print("Missing proof")
        return

    data = {
        "proof": payload["proof"]
    }

    try:
        data_json = json.dumps(data)
        response = requests.post(url=mine_url + "/mine", headers=headers, data=data_json).json()
        return response
    except Exception:
        raise

