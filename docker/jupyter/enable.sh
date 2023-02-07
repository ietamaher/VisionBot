WORKSPACE=$1
AITBOT_CAMERA=${2:-opencv_gst_camera}

# set default swap limit as unlimited
if [[ -z "$AITBOT_JUPYTER_MEMORY_SWAP" ]]
then
	export AITBOT_JUPYTER_MEMORY_SWAP=-1
fi

if [[ -z "$AITBOT_JUPYTER_MEMORY" ]]
then

	sudo docker run -it -d \
	    --restart always \
	    --runtime nvidia \
	    --network host \
	    --privileged \
	    --device /dev/video* \
	    --volume /dev/bus/usb:/dev/bus/usb \
	    --volume /tmp/argus_socket:/tmp/argus_socket \
	    -p 8888:8888 \
	    -v $WORKSPACE:/workspace \
	    --workdir /workspace \
	    --name=aitbot_jupyter \
	    --memory-swap=$AITBOT_JUPYTER_MEMORY_SWAP \
	    --env AITBOT_DEFAULT_CAMERA=$AITBOT_CAMERA \
	    $AITBOT_DOCKER_REMOTE/aibot:jupyter-$AITBOT_VERSION-$L4T_VERSION

else

	sudo docker run -it -d \
	    --restart always \
	    --runtime nvidia \
	    --network host \
	    --privileged \
	    --device /dev/video* \
	    --volume /dev/bus/usb:/dev/bus/usb \
	    --volume /tmp/argus_socket:/tmp/argus_socket \
	    -p 8888:8888 \
	    -v $WORKSPACE:/workspace \
	    --workdir /workspace \
	    --name=aibot_jupyter \
	    --memory=$AITBOT_JUPYTER_MEMORY \
	    --memory-swap=$AITBOT_JUPYTER_MEMORY_SWAP \
	    --env AITBOT_DEFAULT_CAMERA=$AITBOT_CAMERA \
	    $AITBOT_DOCKER_REMOTE/aibot:jupyter-$AITBOT_VERSION-$L4T_VERSION

fi