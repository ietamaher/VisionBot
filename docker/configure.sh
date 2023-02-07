#!/bin/bash

export AITBOT_VERSION=0.0.1

L4T_VERSION_STRING=$(head -n 1 /etc/nv_tegra_release)
L4T_RELEASE=$(echo $L4T_VERSION_STRING | cut -f 2 -d ' ' | grep -Po '(?<=R)[^;]+')
L4T_REVISION=$(echo $L4T_VERSION_STRING | cut -f 2 -d ',' | grep -Po '(?<=REVISION: )[^;]+')


export L4T_VERSION="$L4T_RELEASE.$L4T_REVISION"

if [[ $L4T_VERSION = "32.7.1" ]]
then
	AITBOT_BASE_IMAGE=nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.9-py3
else
	echo "AITBOT_BASE_IMAGE not found for ${L4T_VERSION}.  Please manually set the AITBOT_BASE_IMAGE environment variable. (ie: export AITBOT_BASE_IMAGE=...)"
fi

export AITBOT_BASE_IMAGE
export AITBOT_DOCKER_REMOTE=aibot

echo "AITBOT_VERSION=$AITBOT_VERSION"
echo "L4T_VERSION=$L4T_VERSION"
echo "AITBOT_BASE_IMAGE=$AITBOT_BASE_IMAGE"

./set_nvidia_runtime.sh
sudo systemctl enable docker

# check system memory
SYSTEM_RAM_KILOBYTES=$(awk '/^MemTotal:/{print $2}' /proc/meminfo)

if [ $SYSTEM_RAM_KILOBYTES -lt 3000000 ]
then
    export AITBOT_JUPYTER_MEMORY=500m
    export AITBOT_JUPYTER_MEMORY_SWAP=3G
fi