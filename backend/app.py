from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import math

app = Flask(__name__, static_folder="../")
CORS(app)

INF = float('inf')

def floyd_warshall(nodes, weights):
    n = len(nodes)
    # Initialize dist matrix
    dist = [[INF]*n for _ in range(n)]
    next_hop = [[None]*n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        next_hop[i][i] = i
    for i in range(n):
        for j in range(n):
            w = weights[i][j]
            if w is None:
                continue
            if w == "inf" or w == "∞":
                continue
            try:
                ww = float(w)
            except:
                continue
            dist[i][j] = ww
            next_hop[i][j] = j
    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_hop[i][j] = next_hop[i][k]
    # replace INF with None for JSON
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(None if math.isinf(dist[i][j]) else dist[i][j])
        out.append(row)
    return out, next_hop

@app.route("/api/sample", methods=["GET"])
def sample():
    nodes = ["JFK","LHR","CDG","HND","DXB"]
    weights = [
        [0, 5540, 5836, None, None],
        [None, 0, 344, None, None],
        [None, None, 0, None, None],
        [None, None, None, 0, None],
        [None, None, None, None, 0],
    ]
    return jsonify({"nodes": nodes, "weights": weights})

@app.route("/api/compute", methods=["POST"])
def compute():
    data = request.get_json(force=True)
    nodes = data.get("nodes")
    weights = data.get("weights")
    if not nodes or not weights:
        return jsonify({"error":"Provide 'nodes' and 'weights' in JSON body"}), 400
    if len(nodes) != len(weights):
        return jsonify({"error":"Length of nodes and weights must match"}), 400
    dist, next_hop = floyd_warshall(nodes, weights)
    return jsonify({"nodes": nodes, "distances": dist, "next_hop": next_hop})

# Serve frontend index.html and static files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    root = app.static_folder or "."
    if path == "" or path == "index.html":
        return send_from_directory(root, "index.html")
    return send_from_directory(root, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
