sudo docker build \
    --build-arg BASE_IMAGE=$AIBOT_DOCKER_REMOTE/aibot:base-$AIBOT_VERSION-$L4T_VERSION \
    -t $AITBOT_DOCKER_REMOTE/aibot:camera-$AITBOT_VERSION-$L4T_VERSION \
    -f Dockerfile .