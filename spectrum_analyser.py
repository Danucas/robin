#!/usr/bin/python3
"""
python espectrum analizer

"""

import tkinter as tk
import os, time
from sound_reader import AudioFile




class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x300")
        self.root.configure(background="black")
        self.root.title("RObin Spectrum ANalyzer - ROSAN")
        self.canvas = [None, None]
        self.zones = [None]
        self.selecting = False
        self.au_d = [None, None]
        #track 1 canvas
        self.canvas[0] = tk.Canvas(self.root,
                                   width=(self.root.winfo_screenwidth()),
                                   height=(self.root.winfo_screenheight() - 30),
                                   bg="black")
        self.canvas[0].place(x=0, y=0)
        self.sel_file = tk.Canvas(self.root,
                                  width=(30),
                                  height=(30),
                                  bg="gray")
        #open file track1
        self.sel_file.bind("<Button-1>", lambda e: self.open_file(e, 0))
        self.play_b = tk.Canvas(self.root,
                                width=(30),
                                height=(30),
                                bg="green")
        self.play_b.bind("<Button-1>", lambda e: self.play_file(e, 0))
        self.sel_file.place(x=0, y=120)
        self.play_b.place(x=30, y=120)
        self.canvas[0].bind("<Button-1>", lambda e: self.selectZoneStart(e))
        self.canvas[0].bind("<Motion>", lambda e: self.selectZoneEnd(e, True))
        self.canvas[0].bind("<ButtonRelease-1>",
                            lambda e: self.selectZoneEnd(e, False))

        #Track 2 canvas
        self.canvas[1] = tk.Canvas(self.root,
                                   width=(self.root.winfo_screenwidth()),
                                   height=(self.root.winfo_screenheight() - 30),
                                   bg="black")
        self.canvas[1].place(x=0, y=150)
        #open file track2
        self.sel_file_2 = tk.Canvas(self.root,
                                    width=(30),
                                    height=(30),
                                    bg="gray")
        self.sel_file_2.bind("<Button-1>", lambda e: self.open_file(e, 1))
        self.play_b_2 = tk.Canvas(self.root,
                                  width=(30),
                                  height=(30),
                                  bg="green")
        self.play_b_2.bind("<Button-1>", lambda e: self.play_file(e, 1))
        self.sel_file_2.place(x=0, y=270)
        self.play_b_2.place(x=30, y=270)

    def selectZoneStart(self, ev):
        if self.zones[0] != None:
            self.canvas[0].delete(self.zones[0])
        print(ev, ev.x, ev.y)
        self.zones[0] = self.canvas[0].create_rectangle(ev.x, 1,
                                                        ev.x, 120,
                                                        fill="#2453a3",
                                                        stipple="gray12")
        self.selecting = True
        #self.zones[0] = self.canvas[0].create_rectangle()



    def selectZoneEnd(self, ev, state):
        if state == True and self.selecting == True:
            last = self.canvas[0].coords(self.zones[0])
            x = last[0]
            self.canvas[0].coords(self.zones[0], x, 1, ev.x, 120)
        elif self.selecting == True:
            self.selecting = False
            x = self.canvas[0].coords(self.zones[0])[0]
            width = len(self.au_d[0].data)
            x1 = int((width * x) / 1280)
            x2 = int((width * ev.x) / 1280)
            self.au_d[1] = AudioFile("samps/sample.wav")
            self.au_d[1].data = self.au_d[0].data[x1:x2]
            self.draw_spectrum(self.au_d[1].data, 1)
            print(x, ev.x)
        pass

    def play_file(self, event, c):

        if self.au_d[c] != None:
            self.au_d[c].canvas = self.canvas[c]
            self.au_d[c].play()

    def open_file(self, event, c):
        print("\033[34mFiles: \x1b[38;5;202m")
        files = os.listdir("./recs")
        for i in range(0, len(files), 3):
            try:
                print("{:18}".format(files[i]), "\t", end='')
                print("{:18}".format(files[i + 1]), "\t", end='')
                print("{:18}".format(files[i + 2]), end='')
            except:
                pass
            print()
        inp = input("\033[0m\nChoose a file: ")

        if inp+".wav" in files:
            self.au_d[c] = AudioFile(inp)
            data = self.au_d[c].read_file(inp)
            self.draw_spectrum(data, c)
        else:
            print("No file named ", inp)
            self.open_file(event, c)

    def draw_spectrum(self, sound, c, ini=0, end=None):
        if end == None:
            end = len(sound)
        col = "#a834eb" if c == 0 else "#f2a618"
        chunk = end - ini
        steps = chunk / 1280
        beak = 20
        x = 1
        pos = 0
        last = 0
        self.canvas[c].delete("all")
        while pos < chunk and pos + ini < end:
            y = float(sound[pos + ini]) + 0.5
            y = 120 - int((120 * y) / 1)
            self.canvas[c].create_line(x - 1, last, x, y, fill=col)
            last = y
            x += 1
            pos += int(steps)

        return ini, ini + chunk
