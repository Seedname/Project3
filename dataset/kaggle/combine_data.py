import json
import pathlib
from text_unidecode import unidecode
from collections import defaultdict

def get_movies() -> None:
    movie_names = {}
    actor_movies = {}
    movies_actors = defaultdict(list)

    for file in (path / "movies").glob("*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line: dict = json.loads(line)
            actor_id = list(line.keys())[0]
            movie_ids = [int(movie["id"]) for movie in line[actor_id]]
            actor_movies[int(actor_id)] = movie_ids
            movies = {int(movie["id"]): unidecode(movie["title"]) for movie in line[actor_id]}

            for movie in line[actor_id]:
                movies_actors[int(movie["id"])].append(int(actor_id))

            movie_names |= movies

    with open(path / "actor_movies.json", 'w') as f:
        json.dump(actor_movies, f)
    
    with open(path / "movie_names.json", 'w') as f:
        json.dump(movie_names, f)

    with open(path / "movies_actors.json", 'w') as f:
        json.dump(movies_actors, f)


def get_actors() -> None:
    actor_names = {}
    for file in (path / "outputs").glob("*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = json.loads(line)
            for actor in line:

                actor_names[line[actor][0]["id"]] = unidecode(line[actor][0]["name"])
        
    with open(path / "actor_names.json", "w") as f:
        json.dump(actor_names, f)



if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    get_movies()
    # get_actors()
