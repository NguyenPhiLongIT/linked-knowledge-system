from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return("This is a linked knowledge system!")

if __name__ == "__main__":
    app.run(debug=True)