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
RUN apt-get install -y wget

RUN mkdir "manim_rtvf383_final"
RUN mkdir "tmp"
WORKDIR manim_rtvf383_final
RUN wget https://raw.githubusercontent.com/ScaryMonkey83/manim_rtvf383_final/continuation/manim_music.py
RUN wget https://raw.githubusercontent.com/ScaryMonkey83/manim_rtvf383_final/continuation/requirements_preprocess.txt
RUN wget https://raw.githubusercontent.com/ScaryMonkey83/manim_rtvf383_final/continuation/scripts/begin_preprocess.sh

RUN python3.9 -m venv venv
RUN source venv/bin/activate && pip install wheel
RUN source venv/bin/activate && pip install setuptools
RUN source venv/bin/activate && pip install --upgrade wheel setuptools pip
RUN source venv/bin/activate && pip install -r requirements_preprocess.txt

CMD ["bash", "begin_preprocess.sh"]