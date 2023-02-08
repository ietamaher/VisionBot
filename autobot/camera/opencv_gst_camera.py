import traitlets
import atexit
import cv2
import threading
import numpy as np
from .camera_base import CameraBase


class OpenCvGstCamera(CameraBase):

    value = traitlets.Any()
    
    # config
    width = traitlets.Integer(default_value=224).tag(config=True)
    height = traitlets.Integer(default_value=224).tag(config=True)
    fps = traitlets.Integer(default_value=30).tag(config=True)
    capture_width = traitlets.Integer(default_value=1280).tag(config=True)
    capture_height = traitlets.Integer(default_value=720).tag(config=True)

    def __init__(self, *args, **kwargs):
        self.value = np.empty((self.height, self.width, 3), dtype=np.uint8)
        super().__init__(self, *args, **kwargs)

        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            re, image = self.cap.read()

            if not re:
                raise RuntimeError('Could not read image from camera.')

            self.value = image
            self.start()
        except:
            self.stop()
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.stop)

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                return jpeg.tobytes()
        else:
            return None

    def _capture_frames(self):
        while True:
            re, image = self.cap.read()
            if re:
                self.value = image
            else:
                break
                
    def _gst_str(self):
        return 'nvarguscamerasrc sensor-mode=3 ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.capture_width, self.capture_height, self.fps, self.width, self.height)

    def start_feed(self):
        if not self.cap.isOpened():
            self.cap.open(self._gst_str(), cv2.CAP_GSTREAMER)
        if not hasattr(self, 'thread') or not self.thread.isAlive():
            self.thread = threading.Thread(target=self.get_frame)
            self.thread.start()

    
    def start(self):
        if not self.cap.isOpened():
            self.cap.open(self._gst_str(), cv2.CAP_GSTREAMER)
        if not hasattr(self, 'thread') or not self.thread.isAlive():
            self.thread = threading.Thread(target=self._capture_frames)
            self.thread.start()

    def stop(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'thread'):
            self.thread.join()
            
    def restart(self):
        self.stop()
        self.start()
        
    @staticmethod
    def instance(*args, **kwargs):
        return OpenCvGstCamera(*args, **kwargs)