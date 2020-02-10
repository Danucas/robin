#!/usr/bin/python3

import librosa
import tkinter as tk
import sounddevice as sd
import soundfile as sf
import json, time
import wave

class AudioFile:

    def __init__(self, filename=None):
        self.filename = filename

    def read_file(self, filename):
        self.data, _ = librosa.load("./recs/" + filename + ".wav", sr=44100)
        sf.write("./recs/" + filename + ".wav", self.data, 44100)
        #wav_file = wave.open("rb.wav", 'r')
        return self.data


    def play(self):
        line = [None]
        line[0] = self.canvas.create_line(2, 1, 2, 120,
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


        #time.sleep(float(len(self.data) / 44100) + 0.5)
        return draw_time_lapse()

        #sd.stop()
