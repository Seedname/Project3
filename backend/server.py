from flask import Flask, request, jsonify, send_from_directory
import pickle
import pathlib
from collections import deque
from flask_cors import CORS
import heapq
import json


path = pathlib.Path(__file__).parent
with open(path / "graph.data", 'rb') as f:
    graph = pickle.load(f)

with open(path / 'avg_popularities.json', 'r') as file:
    avg_popularities = json.load(file)

app = Flask(__name__)

CORS(app,
     resources={r"/*": {"origins": "http://127.0.0.1:5500"}},
     )


@app.route('/bfs', methods=['GET'])
def bfs():
    """
    Breadth-First Search endpoint.
    Expects 'source' and 'target' as query parameters.
    """
    source = int(request.args.get('source'))
    target = int(request.args.get('target'))

    q = deque()
    q.append((source, []))
    seen = {source}
    # source is the current actor, 0 is the distance from source (not needed i think), [] contains the path taken
    while q:
        cur = q.popleft()
        for pair in graph[cur[0]]:
            actor = pair[0]
            movie = pair[1]
            if actor in seen:
                continue
            if actor == target:
                path = cur[1] + [[actor, movie]]
                return jsonify({'path': path}), 200
            seen.add(actor)
            q.append((actor, cur[1]+[[actor, movie]]))

    return jsonify({'path': []}), 200


@app.route('/best-first', methods=['GET'])
# should be renamed to best_first_search. im not doing it because idk if it will brick something
def best_first_search():
    """
    Dijkstra's algorithm endpoint.
    Expects 'source' and 'target' as query parameters.
    """
    source = int(request.args.get('source'))
    target = int(request.args.get('target'))

    # if you are having issues running this it is probably this next line!
    target_pop = avg_popularities.get(str(target), 0)
    pq = []
    heapq.heappush(pq, (0, 0, source, []))
    seen = {source}
    # args: distance, priority (based on popularity), source, path taken
    while pq:
        cur = heapq.heappop(pq)
        for trip in graph[cur[2]]:
            actor = trip[0]
            movie = trip[1]
            popularity = trip[2]
            if actor in seen:
                continue
            if actor == target:
                path = cur[3] + [[actor, movie]]
                return jsonify({'path': path}), 200
            seen.add(actor)
            heapq.heappush(pq, (cur[0]+1, abs(target_pop-popularity),
                           actor, cur[3]+[[actor, movie]]))

    return jsonify({'path': []}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)
