sudo systemctl restart nvargus-daemon

sudo docker run -it -d \
    --restart always \
    --runtime nvidia \
    --network host \
    --privileged \
    --device /dev/video* \
    --volume /dev/bus/usb:/dev/bus/usb \
    --volume /tmp/argus_socket:/tmp/argus_socket \
    --privileged \
    --name=aibot_camera \
    $AITBOT_DOCKER_REMOTE/aibot:camera-$AITBOT_VERSION-$L4T_VERSION