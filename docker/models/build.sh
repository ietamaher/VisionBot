sudo docker build \
    --build-arg BASE_IMAGE=$AITBOT_DOCKER_REMOTE/aibot:base-$AITBOT_VERSION-$L4T_VERSION \
    -t $AITBOT_DOCKER_REMOTE/aibot:models-$AITBOT_VERSION-$L4T_VERSION \
    -f Dockerfile .