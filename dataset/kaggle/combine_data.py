import json
import pathlib
from text_unidecode import unidecode
from collections import defaultdict


def get_movies() -> None:
    movie_names = {}
    actor_movies = {}
    movies_actors = defaultdict(list)
    movie_popularities = {}

    for file in (path / "movies").glob("*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line: dict = json.loads(line)
            actor_id = list(line.keys())[0]
            movie_ids = [int(movie["id"]) for movie in line[actor_id]]
            actor_movies[int(actor_id)] = movie_ids
            movies = {int(movie["id"]): unidecode(movie["title"])
                      for movie in line[actor_id]}

            popularities = {int(movie["id"]): float(
                movie.get("popularity", -1)) for movie in line[actor_id]}

            for movie in line[actor_id]:
                movies_actors[int(movie["id"])].append(int(actor_id))

            movie_names |= movies
            movie_popularities |= popularities

    with open(path / "actor_movies.json", 'w') as f:
        json.dump(actor_movies, f)

    with open(path / "movie_names.json", 'w') as f:
        json.dump(movie_names, f)

    with open(path / "movies_actors.json", 'w') as f:
        json.dump(movies_actors, f)

    with open(path / "movies_popularities.json", 'w') as f:
        json.dump(movie_popularities, f)

    # get average movie popularity for each actor
    with open('dataset/kaggle/movies_popularities.json', 'r') as file:
        movie_popularities = json.load(file)

    with open('dataset/kaggle/actor_movies.json', 'r') as file:
        actor_movies = json.load(file)

    actor_avg_popularity = {}

    for key, value in actor_movies.items():
        movie_count = 0
        total_popularity = 0

        for movie in value:
            movie_count += 1
            total_popularity += movie_popularities.get(str(movie))

        avg_popularity = total_popularity/movie_count
        actor_avg_popularity[key] = avg_popularity

    with open(path / "avg_popularities.json", 'w') as f:
        json.dump(actor_avg_popularity, f)


def get_actors_sorted() -> None:
    actor_names = {}
    with open(path / "movies_actors.json", 'r') as f:
        actors_movies = json.load(f)

    for file in (path / "outputs").glob("*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = json.loads(line)
            for actor in line:
                if str(line[actor][0]["id"]) not in actors_movies:
                    continue

                actor_names[unidecode(line[actor][0]["name"]).strip(
                ).lower()] = line[actor][0]["id"]

    sorted_keys = sorted(list(actor_names.keys()))

    # Sorted Dictionary
    sorted_names = {i: actor_names[i] for i in sorted_keys}
    with open(path / "actor_names_sorted.json", "w") as f:
        json.dump(sorted_names, f)


def get_actors() -> None:
    actor_names = {}
    for file in (path / "outputs").glob("*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = json.loads(line)
            for actor in line:

                actor_names[int(line[actor][0]["id"])] = unidecode(
                    line[actor][0]["name"]).strip()

    with open(path / "id_actors_names.json", "w") as f:
        json.dump(actor_names, f)


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    # get_movies()
    # get_actors()
    get_actors_sorted()
