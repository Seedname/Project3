from flask import Flask, request, jsonify, send_from_directory
import pickle
import pathlib
from collections import deque
from flask_cors import CORS
import heapq
import json
import time

path = pathlib.Path(__file__).parent
with open(path / "graph.data", 'rb') as f:
    graph = pickle.load(f)

with open(path / 'avg_popularities.json', 'r') as file:
    avg_popularities = json.load(file)

app = Flask(__name__)

CORS(app,
     resources={r"/*": {"origins": "http://127.0.0.1:5501"}},
     )


@app.route('/bfs', methods=['GET'])
def bfs():
    """
    Breadth-First Search endpoint.
    Expects 'source' and 'target' as query parameters.
    """
    source = int(request.args.get('source'))
    target = int(request.args.get('target'))

    # q args: source, path taken
    q = deque()
    q.append((source, []))

    # seen will contain all seen vertices (actors)
    seen = {source}
    while q:
        cur = q.popleft()
        for pair in graph[cur[0]]:
            actor = pair[0]
            movie = pair[1]
            # no need to check seen actors
            if actor in seen:
                continue
            if actor == target:
                # update path and return
                path = cur[1] + [[actor, movie]]
                return jsonify({'path': path}), 200
            seen.add(actor)
            # update path and append new actor to q
            q.append((actor, cur[1]+[[actor, movie]]))

    return jsonify({'path': []}), 200


@app.route('/best-first', methods=['GET'])
def best_first_search():
    """
    Best-first search algorithm endpoint.
    Expects 'source' and 'target' as query parameters.
    """
    source = int(request.args.get('source'))
    target = int(request.args.get('target'))

    target_pop = avg_popularities.get(str(target), 0)

    pq = []
    # pq args: distance, priority (based on popularity), source, path taken
    heapq.heappush(pq, (0, 0, source, []))

    # seen will contain all seen vertices (actors)
    seen = {source}
    while pq:
        cur = heapq.heappop(pq)
        for trip in graph[cur[2]]:
            actor = trip[0]
            movie = trip[1]
            popularity = trip[2]
            # no need to check a vertex that was already seen
            if actor in seen:
                continue
            if actor == target:
                # update path and return
                path = cur[3] + [[actor, movie]]
                return jsonify({'path': path}), 200
            seen.add(actor)

            # abs(target_pop-popularity) is our priority heuristic
            heapq.heappush(pq, (cur[0]+1, abs(target_pop-popularity),
                           actor, cur[3]+[[actor, movie]]))

    return jsonify({'path': []}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)
