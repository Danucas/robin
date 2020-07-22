#!/usr/bin/env bash

# Download buildozer source
git clone https://github.com/kivy/buildozer.git
cd buildozer
# Compile and install from source
sudo python setup.py
cd ..
# Remove the cloned repo
rm -rf buildozer

# Update and install JDK
sudo apt update
sudo apt install -y git zip unzip \
    openjdk-8-jdk python3-pip autoconf \
    libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev

# Python dependencies for buildozer build
pip3 install --user --upgrade cython virtualenv

sudo apt-get install cython

echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
source ~/.bashrc
#pip3 install --user python-for-android
