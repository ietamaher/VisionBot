ARG BASE_IMAGE=aibot-base:jp463
FROM ${BASE_IMAGE}
RUN echo "BASE_IMAGE: ${BASE_IMAGE}" 
CMD cd ${AIBOT_REPO_DIR} && python3 scripts/zmq_camera_publisher.py