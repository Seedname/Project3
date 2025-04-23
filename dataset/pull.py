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


def get_movies_from_themoviedb_id(themoviedb_id: str) -> dict:
    """
        This function gets the movies that an actor has acted in based on their themoviedb_id
    """

    url = f"https://api.themoviedb.org/3/person/{themoviedb_id}/movie_credits?language=en-US"

    headers = {"Authorization": f"Bearer {READ_TOKEN}",
               "accept": "application/json"}
    
    req = requests.get(url, headers=headers)
    
    if not req.ok:
        raise ValueError(req.json()["status_message"])
    
    res: dict = req.json()

    # if "cast" is not in the response, they haven't acted in any movies
    if "cast" not in res or len(res["cast"]) == 0:
        raise LookupError(f"{themoviedb_id} did not act in any movies")
    
    return {themoviedb_id: res["cast"]}


def get_person_from_imdb_id(imdb_id: str) -> dict:
    """
        This function gets an actor's themoviedb id based on their imdb_id
    """

    url = f"https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id"
    headers = {"Authorization": f"Bearer {READ_TOKEN}",
               "accept": "application/json"}
    
    req = requests.get(url, headers=headers)
    
    if not req.ok:
        raise ValueError(req.json()["status_message"])
    
    res: dict = req.json()

    if "person_results" not in res or len(res["person_results"]) == 0:
        raise LookupError(f"Person not found for {imdb_id}")
    
    return {imdb_id: res["person_results"]}
