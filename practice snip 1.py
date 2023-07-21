from flask import Flask, jsonify
import os
import time
import threading

# Create the Flask app
app = Flask(__name__)

# Middleware
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

# Load and initialize generators before starting server
def load_generators():
    # Your implementation of loading generators goes here
    # If you have any asynchronous tasks, you can use threading.Thread or asyncio

# Client limit reset
def client_limit_reset():
    while True:
        offenders = {}
        clients = {}

        # Your implementation of checking and resetting client limits goes here

        time.sleep(settings.resetInterval)

# Routes
@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/api')
def api():
    return jsonify({'message': 'This is the API endpoint.'})

@app.route('/getStats')
def get_stats():
    return jsonify({'message': 'This is the stats endpoint.'})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == "__main__":
    # Load and initialize generators before starting the server
    load_generators_thread = threading.Thread(target=load_generators)
    load_generators_thread.start()

    # Start the client limit reset thread
    client_limit_reset_thread = threading.Thread(target=client_limit_reset)
    client_limit_reset_thread.start()

    # Start the Flask development server
    app.run(host='0.0.0.0', port=settings.port)
