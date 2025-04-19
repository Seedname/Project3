import json
import pathlib
from collections import defaultdict
import pickle


def main() -> None:
    graph = defaultdict(list)

    with open(path / "actor_movies.json", 'r') as f:
        actor_movies = json.load(f)
    
    with open(path / "movies_actors.json", 'r') as f:
        movies_actors = json.load(f)

    for actor in actor_movies:
        # get all the movies this actor has been in
        for movie in actor_movies[actor]:
            for other_actor in movies_actors[str(movie)]:
                if int(actor) == int(other_actor): continue
                # get all the other actors in that movie (not including itself)
                graph[int(actor)].append((int(other_actor), int(movie)))

    with open(path / "graph.data", 'wb') as f:
        pickle.dump(graph, f)

if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    main()