#!/usr/bin/env python3
#run this on termial
# python setup.py build_ext --inplace --verbose

import sys
sys.path.insert(0, "./")
import cython
import subprocess

from flask import Flask, jsonify, request
from flask_cors import CORS
import chess

import search
app = Flask(__name__)
# Enable CORS for specific origins
CORS(app, resources={r"/*": {"origins": "https://chessbot.local"}})
@app.route('/move', methods=['POST'])
def receive_data():
    fen = request.json
    board = chess.Board(fen)
    board.push(search.play_min_maxN(board,3))
    return jsonify({"message": board.fen()}), 200
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5000)




















