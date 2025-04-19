from flask import Flask, request, jsonify
import pickle
import pathlib
from collections import deque
import copy
from flask_cors import CORS


path = pathlib.Path(__file__).parent
with open(path / "graph.data", 'rb') as f:
    graph = pickle.load(f)

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


    q=deque()
    q.append((source,[]))
    seen=set()
    #source is the current actor, 0 is the distance from source (not needed i think), [] contains the path taken
    while q:
        cur=q.popleft()
        for pair in graph[cur[0]]:
            actor=pair[0]
            movie=pair[1]
            if actor in seen:
                continue
            seen.add(cur[0])
            if actor==target:
                path =  cur[1] + [[actor, movie]]
                return jsonify({'path': path}), 200
            q.append((actor,cur[1]+[[actor,movie]]))
            
    # TODO: Implement BFS algorithm here
    return jsonify({'path': []}), 200

@app.route('/djikstra', methods=['GET'])
def djisktras():
    """
    Dijkstra's algorithm endpoint.
    Expects 'source' and 'target' as query parameters.
    """
    source = request.args.get('source')
    target = request.args.get('target')
    # TODO: Implement Dijkstra's algorithm here
    return jsonify({'message': "Dijkstra's algorithm not implemented yet", 'source': source, 'target': target}), 501

if __name__ == '__main__':
    app.run(debug=True, port=8080)