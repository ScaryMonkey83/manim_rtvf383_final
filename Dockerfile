FROM ubuntu:20.04
MAINTAINER jalehndet11@gmail.com
SHELL ["/bin/bash", "-c"]

# ENV vars
ARG DEBIAN_FRONTEND=noninteractive
ARG AWSAccessKeyId=""
ARG AWSSecretKey=""
ENV AWS_ACCESS_KEY_ID=$AWSAccessKeyId
ENV AWS_SECRET_ACCESS_KEY=$AWSSecretKey

# todo: make sure to remove this in production; for dev only
ENV AWS_BATCH_JOB_ID=0
# todo: make sure to remove this in production; for dev only

# make sure all prereqs are fulfilled
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y libsdl-pango-dev
RUN apt-get install -y python3.9
RUN apt-get install -y python3.9-venv
RUN apt-get install -y g++
RUN apt-get install -y python3.9-dev
RUN apt-get install -y ffmpeg
RUN apt-get install -y inotify-tools
RUN apt-get install -y awscli
RUN apt-get install -y git

# clone the repo holding the code and remove the venv modifications
RUN git clone https://github.com/ScaryMonkey83/manim_rtvf383_final.git
WORKDIR manim_rtvf383_final
RUN git checkout origin/continuation
RUN ls
RUN rm -r venv

# install python virtual environment
RUN python3.9 -m venv venv
RUN source venv/bin/activate && pip install wheel
RUN source venv/bin/activate && pip install setuptools
RUN source venv/bin/activate && pip install --upgrade wheel setuptools pip
RUN source venv/bin/activate && pip install -r requirements.txt

# set up directories
RUN mkdir debug

# run the actual thing
# todo: this needs to be in a CMD ?????
RUN source venv/bin/activate && \
    python -m manim -qh --fps=60 --disable_caching main.py Video

# update venv with manim cli changes
# RUN git checkout origin/master -- venv/lib/python3.9/site-packages/manim/cli/render/render_options.py
# RUN git checkout origin/master -- venv/lib/python3.9/site-packages/manim/cli/render/commands.py

CMD ["echo", "finished"]