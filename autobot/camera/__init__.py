import os

DEFAULT_CAMERA = os.environ.get('AUTOBOT_DEFAULT_CAMERA', 'opencv_gst_camera')

from .opencv_gst_camera import OpenCvGstCamera
Camera = OpenCvGstCamera