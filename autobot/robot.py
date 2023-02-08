import time
import traitlets
from traitlets.config.configurable import SingletonConfigurable
from .communication import Communication
from .motor import Motor
from .heartbeat import Heartbeat



class Robot(SingletonConfigurable):
    left_motor = traitlets.Instance(Motor)
    right_motor = traitlets.Instance(Motor)

    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        self.left_motor = Motor(parent=self)
        self.right_motor = Motor(parent=self)
        self.speed = 0
        self.mode = 0
        self.comm = Communication('/dev/ttyACM0', 115200)
        self.data2receive = [0] * 14  # Initialize an array of 14 elements with 0
        self.data2send = [self.left_motor.value, self.right_motor.value, self.mode]

    def update_motor_value(self):
        self.data2send = [self.left_motor.value, self.right_motor.value, self.mode]
        print(self.data2send)
        self.data2receive = self.comm.send_receive_Data(self.data2send)
        print(self.data2receive)

    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed
        self.right_motor.value = right_speed

    def forward(self, speed=None, duration=None):
        if speed is None:
            speed = self.speed
        else:
            self.speed = speed
        self.left_motor.value = speed
        self.right_motor.value = speed

    def backward(self, speed=None):
        if speed is None:
            speed = self.speed
        else:
            self.speed = speed
        self.left_motor.value = -speed
        self.right_motor.value = -speed

    def left(self, speed=None):
        if speed is None:
            speed = self.speed
        else:
            self.speed = speed
        self.left_motor.value = -speed
        self.right_motor.value = speed

    def right(self, speed=None):
        if speed is None:
            speed = self.speed
        else:
            self.speed = speed

        self.left_motor.value = speed
        self.right_motor.value = -speed

    def stop(self, speed=None):
        self.left_motor.value = 0
        self.right_motor.value = 0
