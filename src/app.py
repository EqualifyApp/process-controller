import os
import signal
from utils.watch import configure_logger
from flask import Flask, render_template, jsonify
import threading
from scan_axe import yeet_axes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app = Flask(__name__)

output = []
configure_logger(output)

status = 'stopped'
output = []
executor_thread = None

stop_flag = threading.Event()


def run_yeet_axes():
    global status
    global output
    status = 'running'
    try:
        yeet_axes(stop_flag)
    finally:
        status = 'stopped'


@app.route('/')
def index():
    most_recent_url = output[-1]['message'] if output else ''
    return render_template('index.html', status=status, output=output, most_recent_url=most_recent_url)


@app.route('/start', methods=['POST'])
def start():
    global executor_thread
    if status == 'stopped':
        executor_thread = threading.Thread(target=run_yeet_axes)
        executor_thread.start()
    return 'OK'


@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag.set()
    return jsonify({'status': 'success', 'message': 'Stop signal sent'}), 200


@app.route('/get_recent_log')
def get_recent_log():
    most_recent_log = output[-1]['message'] if output else ''
    return jsonify({'most_recent_log': most_recent_log})


@app.route('/get_status')
def get_status():
    return status



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Add the host parameter

