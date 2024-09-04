from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def list():
    nodes = [   {"label": "node0", "name": "Hệ điều hành"}, 
                {"label": "node1", "name": "Nhiệm vụ"}, 
                {"label": "node2", "name": "Quản lý tiến trình"}, 
                {"label": "node3", "name": "Hệ thống máy tính"}
    ]
    edges = [   {"source": "node0", "target": "node1"},
                {"source": "node0", "target": "node2"},
                {"source": "node0", "target": "node3"},
    ]
    return jsonify({"nodes": nodes, "edges": edges})


if __name__ == "__main__":
    app.run(debug=True)