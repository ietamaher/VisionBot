import json
from flask import Flask, render_template, jsonify, request  # pip install Flask
from flask_socketio import SocketIO, emit, send  # pip install Flask-SocketIO
from flask import Response
from flask import Flask, render_template
import threading
import traitlets
from autobot import Camera
from autobot import Robot
import time


class FlaskApp:
    def __init__(self):

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.socketio = SocketIO(self.app, logger=True, engineio_logger=True)
        self.camera = Camera.instance(width=640, height=480)
        self.robot = Robot()
        self.camera.start_feed()
        self.start()
        self.frontLimitDistance = 0
        self.rearLimitDistance = 0

        # Start a new thread to send updated data every 5 seconds
        self.data_thread = threading.Thread(target=self.send_updated_data)
        self.data_thread.start()

    def run(self, host='0.0.0.0', port=5000):
        self.socketio.run(self.app, host=host, port=port, allow_unsafe_werkzeug=True)

    def start(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/tp1')
        def tp1():
            return render_template('tp1.html')

        @self.app.route('/tp2')
        def tp2():
            return render_template('tp2.html')

        @self.app.route('/settings')
        def settings():
            return render_template('settings.html')

        # route for video streaming
        @self.app.route('/video_feed')
        def video_feed():
            return Response(gen(self.camera),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        def gen(camera):
            while True:
                frame = camera.get_frame()
                if frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        def mode_to_code(mode):
            if mode == 'automatic':
                return 1
            elif mode == 'semi-automatic':
                return 2
            elif mode == 'manual':
                return 3
            else:
                return 0

        def jog_to_code(mode):
            if mode == 'web-jog':
                return 1
            elif mode == 'rc-jog':
                return 2
            elif mode == 'gamepad':
                return 3
            else:
                return 0

        @self.socketio.on('start_camera')
        def handle_start_camera():
            print("start_camera")
            self.camera.start_feed()

        @self.socketio.on('stop_camera')
        def handle_stop_camera():
            self.camera.stop()

        # socketio events for buttons and sliders
        @self.socketio.on('connect')
        def handle_connect():
            print("Client connected")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print("Client disconnected")

        @self.socketio.on('start_move_forward')
        def handle_start_move_forward():
            # code to start moving the motor forward
            self.robot.forward()
            print("Starting to move forward")

        @self.socketio.on('stop_move_forward')
        def handle_stop_move_forward():
            self.robot.stop()
            print("Stopping to move forward")

        @self.socketio.on('move_backward')
        def handle_move_backward():
            # code to send command to move motors backward
            self.robot.backward()
            print("Moving backward")

        @self.socketio.on('move_left')
        def handle_move_left():
            # code to send command to move motors left
            self.robot.left()
            print("Moving left")

        @self.socketio.on('move_right')
        def handle_move_right():
            # code to send command to move motors right
            self.robot.right()
            print("Moving right")

        @self.socketio.on('message')
        def handle_message(message):
            send(message)

        @self.socketio.on('set_speed')
        def handle_set_speed(speed):
            self.robot.speed = float(speed)  # Store the received speed in the first element of the data array
            print("Current speed:", self.robot.speed)
            #self.robot.update_data_string()

        @self.socketio.on('set_mode')
        def handle_set_mode(mode):
            self.robot.data_values[1] = mode_to_code(
                mode)  # Store the received speed in the first element of the data array
            print("Current mode:", self.robot.data_values[1])
            self.robot.update_data_string()

        @self.socketio.on('set_jog')
        def handle_set_jog(jog):
            self.robot.data_values[2] = jog_to_code(
                jog)  # Store the received speed in the first element of the data array
            print("Current jog:", self.robot.data_values[2])
            self.robot.update_data_string()

        @self.socketio.on('my event')
        def handle_my_custom_event(json):
            print('received json: ' + str(json))

        @self.app.route('/save_settings', methods=['POST'])
        def save_settings():
            self.robot.data_values[3] = request.json['frontLimitDistance']
            self.robot.data_values[4] = request.json['rearLimitDistance']
            data = {'frontLimitDistance': self.robot.data_values[3], 'rearLimitDistance': self.robot.data_values[4]}
            with open('settings.txt', 'w') as outfile:
                json.dump(data, outfile)
            #self.robot.update_data_string()
            return 'Settings saved'

        @self.app.route('/get_settings')
        def get_settings():
            with open('settings.txt') as file:
                data = json.load(file)
            return jsonify(data)

    def send_updated_data(self):
        while True:
            self.socketio.emit('update_data', {'data': self.robot.data2receive})
            time.sleep(5)




if __name__ == '__main__':
    app = FlaskApp()
    app.run(host='0.0.0.0', port=5000)
