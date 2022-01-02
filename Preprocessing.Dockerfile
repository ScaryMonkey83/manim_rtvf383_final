FROM ubuntu:20.04
MAINTAINER jalehndet11@gmail.com
SHELL ["/bin/bash", "-c"]

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y python3.9
RUN apt-get install -y python3.9-venv
RUN apt-get install -y g++
RUN apt-get install -y python3.9-dev
RUN apt-get install -y ffmpeg
RUN apt-get install -y inotify-tools
RUN apt-get install -y git