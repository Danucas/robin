#!/usr/bin/python3
"""
WAV format reader
"""

import librosa
import tkinter as tk
import sounddevice as sd
import soundfile as sf
import json, time
import wave

class AudioFile:
    """
    Store the signal from wav format in
    self.data
    """
    def __init__(self, filename=None):
        """
        Assing a name to reach the file
        """
        self.filename = filename

    def read_file(self, filename):
        """
        Reads the .wav file from ./recs at 44100 frame rate
        """
        self.data, _ = librosa.load("./recs/" + filename + ".wav", sr=44100)
        sf.write("./recs/" + filename + ".wav", self.data, 44100)
        return self.data

    def play(self):
        """
        Plays the audio file and render a process line in the Track
        """
        line = [None]
        line[0] = self.canvas.create_line(
            2, 1, 2, 120,
            fill="#3debe5",
            width=2)
        time.sleep(0.5)
        def draw_time_lapse():
            init = 0
            end = int(len(self.data))
            width = 1280
            pos = 0
            lapse = 16
            chunk = int(len(self.data) / width) * lapse
            t_s = float(chunk / 44100) * 1
            print("chunk", chunk, "t_s", t_s)
            sd.play(self.data[init:end], 44100, blocking=False)
            while pos < width:
                end = init + chunk
                self.canvas.move(line[0], lapse, 0)
                self.canvas.update()
                #sd.stop()
                time.sleep(t_s)
                pos += lapse
                init += chunk
            sd.stop()
            print("end pos")
            print("end...")
        return draw_time_lapse()
