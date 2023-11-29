import os

from flask import Flask, jsonify, send_from_directory
import threading as thread
from waitress import serve
from termcolor import colored

from backend.src.flask.services.process_mining_service import ProcessMiningService

PROCESS_MINING_SERVICE = ProcessMiningService()
app = Flask('ORCA')


@app.route('/')
def index():
    return send_from_directory('frontend/dist/', 'index.html')


# If Render.com preview, show some info about the deployment to avoid confusion
@app.route('/render-config')
def render_sha_available():
    if 'RENDER_GIT_BRANCH' in os.environ and 'RENDER_GIT_COMMIT' in os.environ:
        return jsonify({'branch': os.environ['RENDER_GIT_BRANCH'], 'commit': os.environ['RENDER_GIT_COMMIT']})
    else:
        return jsonify({})


@app.route('/<path:file>')
def serve_static_file(file):
    return send_from_directory('frontend/dist/', file)


@app.route('/variants')
def calculate():
    return jsonify(PROCESS_MINING_SERVICE.get_variants())


@app.route('/patient-attributes')
def get_patient_attributes():
    return jsonify(PROCESS_MINING_SERVICE.get_patient_attributes())


if __name__ == '__main__':
    def run_server():
        # List of ports to attempt to allocate.
        print("Running ORCA 🐋: ")
        for port in [80, 8080, 8000, 8081]:
            try:
                print(f'🟢 - Server running at', colored(f'http://127.0.0.1:{port}', 'green'))
                serve(app, host='0.0.0.0', port=port)
            except Exception:
                # This print clears the prior line, which is always the 'Server running ...' message
                print('\033[A                             \033[A')
                print(f'🔴 - Taking', colored(f'port {port} failed', 'red'), ', trying next port ...')
        print('All pre-defined ports have failed. Either change them or check your system!')


    # Create a separate process for running the server
    try:
        server_process = thread.Thread(target=run_server)
    except Exception as e:
        raise e

    with open('backend/files/orca-ascii.txt', mode='r') as ascii:
        print(colored(ascii.read(), "blue"))

    server_process.start()
