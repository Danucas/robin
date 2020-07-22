#!/usr/bin/env bash

# install pip3 and python required dependencies for
# Audio processing
sudo python3 -m pip install librosa tk sounddevice soundfile wave

# Install Audio codecs and libraries
sudo apt-get install ffmpeg
sudo apt-get install libportaudio2
sudo apt-get install libasound-dev
