from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True
)

@app.route('/')
def hello():
    return jsonify({'message': 'hello internal'}), 500

app.run()

