from pyduinobridge import Bridge_py  # pip install pyduinobridge   pip install pyserial


class Communication:

    def __init__(self, port, baudrate):
        self.baudRate = baudrate
        self.serPort = port
        self.myBridge = Bridge_py()
        self.myBridge.begin(self.serPort, self.baudRate, numIntValues_FromPy=12, numFloatValues_FromPy=0)
        self.myBridge.setSleepTime(.2)


    def send_receive_Data(self, data2send):
        # Prepare data2send
        string_data2send = '<MM,' + ','.join(str(x) for x in data2send) + '>'
        print(string_data2send)
        string_data2send_array = [string_data2send]
        dataFromArduino = self.myBridge.writeAndRead_Strings(string_data2send_array)
        # The values received are
        # arduino_data = dataFromArduino[0].split()
        # self.data2receive[0] = arduino_data[2]
        # self.data2receive[1] = arduino_data[4]
        # self.data2receive[2] = arduino_data[6]
        return dataFromArduino
