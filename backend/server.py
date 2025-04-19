from flask import Flask, request, jsonify
import pickle
import pathlib

path = pathlib.Path(__file__).parent
with open(path / "graph.data", 'rb') as f:
    graph = pickle.load(f)

app = Flask(__name__)

@app.route('/bfs', methods=['GET'])
def bfs():
    """
    Breadth-First Search endpoint.
    Expects 'source' and 'target' as query parameters.
    """
    source = request.args.get('source')
    target = request.args.get('target')
    # TODO: Implement BFS algorithm here
    return jsonify({'message': 'BFS not implemented yet', 'source': source, 'target': target}), 501

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
    app.run(debug=True)