# NOTE:
# currently only runs proof_of_work algo a single time
import hashlib
import requests
import json
import random
import sys
import time

from uuid import uuid4

from timeit import default_timer as timer

import random
import os

from dotenv import load_dotenv

load_dotenv()


def proof_of_work(data):

    start = timer()

    print("Searching for next proof")

    last_proof = data["proof"]
    difficulty = data["difficulty"]
    # start at a random point
    proof = last_proof * random.randint(0, 100)

    valid_proof(last_proof, difficulty, proof)
    # while valid_proof(last_proof, difficulty, proof) is False:
    #     proof += 1

    # print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, difficulty, proof):
    # hash the last_proof and the attempted proof together
    # then check to see if it has the required zeros

    zeros = '0' * difficulty    

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[:difficulty] == zeros

if __name__ == '__main__':
    node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    coins_mined = 0
    API_KEY = os.getenv("API_KEY")
    headers = {"Authorization": f"Token {API_KEY}"}

    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof", headers=headers)
        data = r.json()

        # sleep for 1 second
        time.sleep(1)

        new_proof = proof_of_work(data)

        break

        post_data = {"proof": new_proof}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
