# from https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch  
# PyTorch Container for Jetson and JetPack

ARG BASE_IMAGE=nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.9-py3
FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive

# ====================
# INSTALL COMMON TOOLS
# ====================
# RUN apt-get install kitware-archive-keyring
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 42D5A192B819C5DA
RUN sed -i 's/deb https:\/\/apt.kitware.com\/ubuntu bionic main/deb https:\/\/apt.kitware.com\/ubuntu bionic main 42D5A192B819C5DA/g' /etc/apt/sources.list
RUN apt-get update 
RUN apt-get install -y net-tools vim cmake


# ==================
# INSTALL TENSORFLOW
# source : https://forums.developer.nvidia.com/t/installing-tensorflow-1-15-on-jetson-nano-2gb-developer-kit-succeeds-but-tensorflow-not-imported/184468/3
# ==================
RUN apt-get update
RUN apt-get install -y --no-install-recommends libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran build-essential python3-pip && rm -rf /var/lib/apt/lists/*
RUN apt-get install python3-pip
RUN pip3 install -U pip testresources setuptools
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip3 install -U numpy==1.19.4 future mock keras_preprocessing keras_applications gast==0.2.1 protobuf pybind11 cython pkgconfig packaging
RUN pip3 install  --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==1.15.5+nv22.01

# RUN apt-get update
# RUN apt-get install -y --no-install-recommends libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran build-essential python3-pip && rm -rf /var/lib/apt/lists/*
# # must have python python3.8 installed https://forums.developer.nvidia.com/t/how-to-support-python3-8/168813/3
# RUN pip3 install -U pip testresources setuptools
# RUN pip3 install  -U setuptools future==0.17.1 mock==3.0.5 keras_preprocessing==1.0.5 keras_applications==1.0.8  --verbose
# RUN pip3 install -U pip testresources setuptools
# RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# RUN pip3 install -U numpy==1.18.5 future mock keras_preprocessing keras_applications gast==0.2.1 protobuf pybind11 cython pkgconfig packaging
# # RUN pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow
# # $JP_VERSION = 461
# # $TF_VERSION = 1.15.5
# # $NV_VERSION = 22.01


		  
#Install system packages required by TensorFlow:
#$ sudo apt-get update
#$ sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
#$ sudo apt-get install python3-pip
#$ sudo pip3 install -U pip testresources setuptools
#$ sudo ln -s /usr/include/locale.h /usr/include/xlocale.h
#$ sudo pip3 install -U numpy==1.19.4 future mock keras_preprocessing keras_applications gast==0.2.1 protobuf pybind11 cython pkgconfig packaging
#$ sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow
# sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==1.15.5+nv22.01
# !!!!!!  h5py<=2.10.0
# Successfully installed absl-py-1.4.0 astor-0.8.1 astunparse-1.6.3 gast-0.3.3 google-pasta-0.2.0 grpcio-1.48.2 importlib-metadata-4.8.3 markdown-3.3.7 numpy-1.18.5 opt-einsum-3.3.0 tensorboard-1.15.0 tensorflow-1.15.5+nv22.1 tensorflow-estimator-1.15.1 termcolor-1.1.0 werkzeug-2.0.3 wrapt-1.14.1 zipp-3.6.0

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
RUN wget https://nodejs.org/dist/v12.13.0/node-v12.13.0-linux-arm64.tar.xz
RUN tar -xJf node-v12.13.0-linux-arm64.tar.xz
RUN cd node-v12.13.0-linux-arm64 && cp -R bin include lib share /usr/local/ && cd .. 
RUN node -v
RUN npm -v
RUN apt-get install -y libffi-dev 
RUN pip3 install jupyter jupyterlab==3.2.9

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
# INSTALL AIBOT
# ==============
ENV AIBOT_REPO_DIR=/opt/aibot
COPY . ${AIBOT_REPO_DIR}
RUN command cd ${AIBOT_REPO_DIR} && python3 setup.py install
