#!/bin/bash

# shellcheck source=/Users/scarymonkey83/AWS/rootkey-4.csv
source "$1"
export AWS_ACCESS_KEY_ID=$AWSAccessKeyId
export AWS_SECRET_ACCESS_KEY=$AWSSecretKey
export AWS_DEFAULT_REGION=us-east-2

sudo apt update
sudo apt-get install -y libsdl-pango-dev
sudo apt-get install -y python3.9
sudo apt install -y python3.9-venv
sudo apt-get install -y g++
sudo apt-get install -y python3.9-dev
sudo apt install -y libav-tools
sudo apt install -y ffmpeg
sudo apt-get install -y inotify-tools
sudo apt-get install -y awscli

git clone https://github.com/ScaryMonkey83/manim_rtvf383_final.git
cd ~/manim_rtvf383_final/ || exit 1
rm -r venv

python3.9 -m venv venv
source venv/bin/activate
pip install wheel
pip install setuptools
pip install --upgrade wheel setuptools pip
pip install -r requirements.txt

git checkout origin/master -- venv/lib/python3.9/site-packages/manim/cli/render/render_options.py
git checkout origin/master -- venv/lib/python3.9/site-packages/manim/cli/render/commands.py
bash scripts/begin.sh

