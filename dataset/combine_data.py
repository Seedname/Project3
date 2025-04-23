import json
import pathlib
from text_unidecode import unidecode
from collections import defaultdict


def get_movies() -> None:
    """
        This function processes the majority of the data that we need
        It does the following:
        1. Get map of an actor id to the movies they've been in
        2. Get a map from a movie id to a movie name
        3. Get a map of the movie id to the actors that have been in that movie
        4. Get a map from the movie id to that movie's popularity
        5. Get the average popularity of the movies that the actor has been in.
    """
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
    with open(path / 'actor_movies.json', 'r') as file:
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
    """
    The purpose of this function is to return a sorted map from actor names to ids 
    to run a prefix binary search on the frontend as an efficient search algorithm
    """
    actor_names = {}
    with open(path / "actor_movies.json", 'r') as f:
        actors_movies = json.load(f)
    for file in (path.parent / "actors").glob("*.txt"):
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
    """
    This function gets a map of actor ids to names
    """
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

def get_actors_urls() -> None:
    """
    This function gets a map of actor ids to the url's of their profile photos
    """
    actor_urls = {}

    with open(path / "data" / "actor_movies.json", 'r') as f:
        actors_movies = json.load(f)

    for file in (path / "outputs").glob("*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = json.loads(line)
            for actor in line:
                if str(line[actor][0]["id"]) not in actors_movies:
                    continue
                if line[actor][0]["profile_path"] == 'null' or line[actor][0]["profile_path"] is None:
                    actor_urls[int(line[actor][0]["id"])] = 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'
                else:
                    actor_urls[int(line[actor][0]["id"])] = f'https://image.tmdb.org/t/p/w1280{line[actor][0]["profile_path"]}'

    with open(path / "id_actors_urls.json", "w") as f:
        json.dump(actor_urls, f)

def get_movies_urls() -> None:
    """
    This function gets a map of movie ids to the url's of their poster photos
    """
    movie_urls = {}

    for file in (path / "movies").glob("*.txt"):
        with open(file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = json.loads(line)
            for movie in line:
                if line[movie][0]["poster_path"] == 'null' or line[movie][0]["poster_path"] is None:
                    movie_urls[int(line[movie][0]["id"])] = 'https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg'
                else:
                    movie_urls[int(line[movie][0]["id"])] = f'https://image.tmdb.org/t/p/w1280{line[movie][0]["poster_path"]}'

    with open(path / "id_movies_urls.json", "w") as f:
        json.dump(movie_urls, f)


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent.joinpath("data")
    # get_movies()
    # get_actors()
    get_actors_sorted()
    # get_actors_urls()
    # get_movies_urls()
