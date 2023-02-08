import traitlets
from traitlets.config.configurable import Configurable


class Motor(Configurable):
    value = traitlets.Float()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @traitlets.observe('value')
    def _observe_value(self, change):
        if self.parent:
            if self == self.parent.left_motor:
                self.parent.left_motor.value = self.value
            elif self == self.parent.right_motor:
                self.parent.right_motor.value = self.value
            self.parent.update_motor_value()
