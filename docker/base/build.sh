cp /etc/apt/trusted.gpg.d/jetson-ota-public.asc ../.. # copy to aibot root

sudo docker build \
    --build-arg BASE_IMAGE=$AITBOT_BASE_IMAGE \
    -t $AITBOT_DOCKER_REMOTE/aibot:base-$AITBOT_VERSION-$L4T_VERSION \
    -f Dockerfile \
    ../..  # aibot repo root as context