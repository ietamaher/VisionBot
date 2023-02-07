# from https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch  
# PyTorch Container for Jetson and JetPack
ARG BASE_IMAGE=nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.9-py3
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive

# ====================
# INSTALL COMMON TOOLS
# ====================
RUN apt-get update && apt-get install -y net-tools vim cmake


# ==================
# INSTALL TENSORFLOW
# ==================

ARG HDF5_DIR="/usr/lib/aarch64-linux-gnu/hdf5/serial/"
ARG MAKEFLAGS=-j6
RUN apt-get update && \

RUN apt-get update && \
    apt-get install -y --no-install-recommends libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran build-essential python3-pip && rm -rf /var/lib/apt/lists/*
		  
RUN pip3 install -U pip testresources setuptools==65.5.0 
RUN pip3 install  -U numpy==1.21.1 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython  futures pkgconfig packaging h5py==3.6.0 --verbose

# $JP_VERSION = 461
# $TF_VERSION = 1.15.5
# $NV_VERSION = 22.01

RUN pip3 install  --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==1.15.5+nv22.01
		  
#Install system packages required by TensorFlow:
# sudo apt-get update
# sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran build-essential && rm -rf /var/lib/apt/lists/*
# sudo apt-get install python3-pip
# sudo pip3 install -U pip testresources setuptools==65.5.0 
# sudo pip3 install -U numpy==1.21.1 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython  futures pkgconfig packaging h5py==3.6.0 --verbose
# sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v$JP_VERSION tensorflow==$TF_VERSION+nv$NV_VERSION
# sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==1.15.5+nv22.01

# ==============
# INSTALL OPENCV
# ==============
COPY jetson-ota-public.asc /etc/apt/trusted.gpg.d/jetson-ota-public.asc
RUN echo "deb https://repo.download.nvidia.com/jetson/common r32.7 main" > /etc/apt/sources.list.d/nvidia-l4t-apt-source.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
            libopencv-python \
    && rm /etc/apt/sources.list.d/nvidia-l4t-apt-source.list \
    && rm -rf /var/lib/apt/lists/*


# =================
# INSTALL GSTREAMER
# =================
RUN apt-get update && \
    apt-get install -y \
    libwayland-egl1 \
    gstreamer1.0-plugins-bad \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    python3-gst-1.0


# =======================
# INSTALL JUPYTER RELATED
# =======================

# Install traitlets (master, to support the unlink() method)
RUN echo -e "\e[48;5;172m Install traitlets \e[0m"
#sudo python3 -m pip install git+https://github.com/ipython/traitlets@master
RUN python3 -m pip install git+https://github.com/ipython/traitlets@dead2b8cdde5913572254cf6dc70b5a6065b86f8

# Install jupyter lab
RUN echo -e "\e[48;5;172m Install Jupyter Lab \e[0m"
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs libffi-dev 
RUN pip3 install jupyter jupyterlab==3.6.1
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager


# Install jupyter_clickable_image_widget
RUN echo "\e[42m Install jupyter_clickable_image_widget \e[0m"
RUN cd && \
    apt-get install -y libssl1.0-dev && \
    git clone https://github.com/jaybdub/jupyter_clickable_image_widget && \
    cd jupyter_clickable_image_widget && \
    git checkout tags/v0.1 && \
    pip3 install -e . && \
    jupyter labextension install js && \
    jupyter lab build
    
# ============================
# INSTALL MISC DEPENDENCIES
# ============================
RUN apt-get update && apt-get install -y supervisor unzip
RUN apt install -y python3-smbus && pip3 install pyzmq


# =================
# INSTALL TORCH2TRT
# =================
ENV TORCH2TRT_REPO_DIR=/opt/
RUN cd ${TORCH2TRT_REPO_DIR} && \
    git clone https://github.com/NVIDIA-AI-IOT/torch2trt && \
    cd torch2trt && \
    python3 setup.py install


# ==============
# INSTALL JETBOT
# ==============
ENV AIBOT_REPO_DIR=/opt/aibot
COPY . ${AIBOT_REPO_DIR}
RUN cd ${AIBOT_REPO_DIR} && python3 setup.py install
