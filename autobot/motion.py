import traitlets
from traitlets.config.configurable import SingletonConfigurable


class Motion(SingletonConfigurable):
    speed = traitlets.Float(default_value=0.0).tag(config=True)
    direction = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, *args, **kwargs):
        super(Motion, self).__init__(*args, **kwargs)

    def move_forward(self, speed):
        """Set the robot to move forward with the specified speed"""
        self.speed = speed
        self.direction = 0.0

    def move_backward(self, speed):
        """Set the robot to move backward with the specified speed"""
        self.speed = -speed
        self.direction = 0.0

    def rotate_left(self, speed):
        """Set the robot to rotate left with the specified speed"""
        self.speed = 0.0
        self.direction = speed

    def rotate_right(self, speed):
        """Set the robot to rotate right with the specified speed"""
        self.speed = 0.0
        self.direction = -speed

    def stop(self):
        """Stop the robot movement"""
        self.speed = 0.0
        self.direction = 0.0