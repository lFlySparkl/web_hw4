from flask import Flask, render_template, request
from datetime import datetime
import socket
import json

app = Flask(__name__)

UDP_SERVER_IP = "127.0.0.1"
UDP_SERVER_PORT = 5000
JSON_FILE_PATH = "storage/data.json"


def send_data_to_udp_server(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = json.dumps(data).encode('utf-8')
    client_socket.sendto(message, (UDP_SERVER_IP, UDP_SERVER_PORT))
    client_socket.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message_text = request.form['message']
        timestamp = str(datetime.now())

        data = {
            timestamp: {
                'username': username,
                'message': message_text
            }
        }

        send_data_to_udp_server(data)

    return render_template('message.html')


# @app.route('/error')
# def error():
@app.route('/<variable>')
def error(variable):
    if variable != "message":
        print(variable)
        return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(port=3000, debug=True)
