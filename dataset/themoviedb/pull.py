import requests
from dotenv import load_dotenv
import os
from text_unidecode import unidecode
from tqdm import tqdm
import time
import pickle

load_dotenv()

READ_TOKEN = os.environ.get("READ_TOKEN", None)

if READ_TOKEN is None:
    raise EnvironmentError("READ_TOKEN environment variable not set")


def get_people_from_page(page: int):
    url = f"https://api.themoviedb.org/3/person/popular?language=en-US&page={page}"
    headers = {"Authorization": f"Bearer {READ_TOKEN}",
               "accept": "application/json"}
    
    req = requests.get(url, headers=headers)
    
    if not req.ok:
        raise ValueError(req.json()["status_message"])
    
    res = req.json()

    return {person["id"]: unidecode(person["name"]) for person in res["results"]}


if __name__ == "__main__":
    people = {}
    
    try:
        for page in tqdm(range(1, 5001)):
            people |= get_people_from_page(page)
    except ValueError:
        print("writing output...")

    with open("out.dump", 'wb') as f:
        pickle.dump(people, f)