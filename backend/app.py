from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def list():
    nodes = [ {"name": "Node 1"}, {"name": "Node 2"}]
    return jsonify(nodes)

if __name__ == "__main__":
    app.run(debug=True)