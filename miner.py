import hashlib
import requests
import json
import random
import sys

from uuid import uuid4

from timeit import default_timer as timer

import random
import os

from dotenv import load_dotenv

load_dotenv()


def proof_of_work(data):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")


    last_proof = data["proof"]
    difficulty = data["difficulty"]
    # start at a random point
    proof = last_proof* random.randint(0, 100)

    valid_proof(last_proof, difficulty, proof)
    # while valid_proof(last_proof, difficulty, proof) is False:
    #     proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, difficulty, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    # hash the last_proof and the attempted proof together
    # then check to see if it has the required zeros

    zeros = '0' * difficulty    

    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[:difficulty] == zeros

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    coins_mined = 0
    API_KEY = os.getenv("API_KEY")
    headers = {"Authorization": f"Token {API_KEY}"}

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof", headers=headers)
        data = r.json()
        # first i can get all the data i need

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
