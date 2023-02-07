sudo docker run -it -d \
    --restart always \
    --runtime nvidia \
    --network host \
    --privileged \
    --name=aibot_display \
    $AITBOT_DOCKER_REMOTE/aibot:display-$AITBOT_VERSION-$L4T_VERSION