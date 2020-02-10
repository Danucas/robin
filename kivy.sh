#!/bin/bash

#install buildozer
git clone https://github.com/kivy/buildozer.git
cd buildozer
sudo python setup.py
cd ..
rm -rf buildozer

sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev
pip3 install --user --upgrade cython virtualenv

sudo apt-get install cython

echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
source ~/.bashrc
#pip3 install --user python-for-android
