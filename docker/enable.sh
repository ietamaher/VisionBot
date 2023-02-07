source configure.sh

JUPYTER_WORKSPACE=${1:-$HOME}  # default to $HOME
AIBOT_CAMERA=${2:-opencv_gst_camera}  # default to opencv

if [ "$AIBOT_CAMERA" = "zmq_camera" ]
then
	./camera/enable.sh
fi

./display/enable.sh
./jupyter/enable.sh $JUPYTER_WORKSPACE $AIBOT_CAMERA