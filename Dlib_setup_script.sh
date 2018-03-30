###Steps in setting up dlib, cmake and facial-recognition

sudo apt-get -y update && sudo apt-get install python3-pip \
&& sudo apt-get install -y --fix-missing \
build-essential \
cmake \
gfortran \
git \
wget \
curl \
graphicsmagick \
libgraphicsmagick1-dev \
libatlas-dev \
libavcodec-dev \
libavformat-dev \
libgtk2.0-dev \
libjpeg-dev \
liblapack-dev \
libswscale-dev \
pkg-config \
python3-dev \
python3-numpy \
software-properties-common \
zip \
&& sudo apt-get clean && sudo rm -rf /tmp/* /var/tmp/* \

 cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
cd dlib/ && mkdir build && cd build/ && \
sudo cmake .. -DDLIB_USE_CUDA=0 -DUSE_AVX_INSTRUCTIONS=1 && sudo cmake --build . \
&& cd .. \
&& sudo python3 setup.py install --yes USE_AVX_INSTRUCTIONS --no DLIB_USE_CUDA \

### Install python boost engine

sudo apt-get install libboost-all-dev
