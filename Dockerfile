FROM debian:latest

MAINTAINER sargis@yonan.org

#Face classificarion dependencies & web application from apt-get (Debian) and pip
RUN apt-get -y update && apt-get install -y python python-pip python-dev python-tk vim procps curl
RUN pip install numpy scipy scikit-learn pillow tensorflow pandas h5py opencv-python==3.2.0.8 keras statistics pyyaml pyparsing cycler matplotlib Flask

# literally copy the file structure from local to image
COPY . /.

