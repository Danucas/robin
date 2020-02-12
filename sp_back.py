#!/usr/bin/python3
"""
RObin Spectrum ANalizer -- ROSAN -- module

"""

import tkinter as tk
import os, time
from sound_reader import AudioFile
import sounddevice as sd

class Track:
    """
    Track object, contains track widgets and tools
    :filename: Is used for name the track
    :nid: used to identify modify and track the object and it's behavior
    :zone: contains a selected chunk of data
    :canvas: the main container for the track view
    :sel_file: run the file selection function
    :play: play the complete track data
    """
    instance = 0
    def __init__(self, root, filename=None):
        Track.instance += 1
        if filename == None:
            filename = "Track-" + str(Track.instance)
        self.filename = filename
        self.nid = Track.instance - 1
        self.zone = None
        root.root.geometry("1280x{}".format(150 * Track.instance))
        #track 1 canvas
        self.canvas = tk.Canvas(root.root,
                                   width=(root.root.winfo_screenwidth()),
                                   height=(150),
                                   bg="black", bd=0, relief="ridge",
                                  highlightthickness=0)
        self.canvas.place(x=0, y=(self.nid * 150))
        #open file track1
        self.sel_file = tk.Canvas(self.canvas,
                                  width=(90),
                                  height=(30),
                                  bg="black", cursor="hand2",
                                  bd=0, relief="ridge",
                                  highlightthickness=0)
        root.round_rectangle(3, 3, 87, 27,
                             self.sel_file,
                             radius=20, fill="blue")
        self.sel_file.create_text(70, 15,
                                  text='Open file',
                                  anchor='e', fill="white")

        self.sel_file.bind("<Button-1>", lambda e: root.open_file(e, self.nid))
        self.sel_file.place(x=0, y=120)

        #play button
        self.play_b = tk.Canvas(self.canvas,
                                width=(45),
                                height=(30),
                                bg="black", cursor="hand2",
                                bd=0, relief="ridge",
                                highlightthickness=0)
        root.round_rectangle(3, 3, 27, 27,
                             self.play_b,
                             radius=20, fill="#32a852")
        self.play_b.create_text(20, 15,
                                  text='>',
                                  anchor='e', fill="white")
        root.round_rectangle(3, 3, 27, 27,
                             self.play_b,
                             radius=20, fill="#32a852")
        self.play_b.bind("<Button-1>", lambda e: root.play_file(e, self.nid))
        self.play_b.create_text(20, 15,
                                  text='>',
                                  anchor='e', fill="white")
        self.play_b.place(x=90, y=120)
        self.canvas.bind("<Button-1>",
                            lambda e: root.selectZoneStart(e, self.nid))
        self.canvas.bind("<Motion>",
                            lambda e: root.selectZoneEnd(e, True, self.nid))
        self.canvas.bind("<ButtonRelease-1>",
                            lambda e: root.selectZoneEnd(e, False, self.nid))

class Sample:
    """
    Sample object
    :data: The selected audio signal
    :nid: used to track, modify and interact with the data and view
    :window: the pop up window displayed
    :canvas: the main container for the sample view handles the drawing
    :play: plays the sample audio data
    """
    def __init__(self, root, data, nid):
        """
        Inits the attributes, view and listeners
        """
        self.data = data
        self.nid = nid
        self.window = tk.Toplevel(root.root)
        self.window.geometry("800x150+0+230")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.window.title("Sample from track {}".format(nid + 1))
        self.canvas = tk.Canvas(self.window, width=800,
                                height=150, bg="black",
                                bd=0, relief="ridge",
                                highlightthickness=0)
        self.play = tk.Canvas(self.canvas, width=30, height=30,
                              cursor="hand2",
                              bg="black",bd=0, relief="ridge",
                              highlightthickness=0)
        root.round_rectangle(3, 3, 27, 27,
                             self.play,
                             radius=20, fill="#32a852")
        self.play.create_text(20, 15,
                              text='>',
                              anchor='e', fill="white")
        self.play.bind("<Button-1>", lambda e: self.play_sound(e))
        self.play.place(x=0, y=120)

        self.canvas.pack()
        self.draw_sample()

    def on_close(self):
        """
        Removes the sample instances and view
        """
        print("deleting", self.nid, "sample")
        self.window.destroy()
        del self

    def play_sound(self, evn):
        """
        Plays the sample chunk of data
        """
        line = [None]
        line[0] = self.canvas.create_line(2, 1, 2, 120,
                                          fill="#3debe5",
                                          width=2)
        def draw_time_lapse():
            """
            Draws the time lapsing line
            """
            init = 0
            end = int(len(self.data))
            width = 800
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
        draw_time_lapse()
        sd.play(self.data, 44100)

    def draw_sample(self):
        """
        Draws the spectrogram for the sample data
        """
        width = len(self.data)
        col = "#4287f5"
        chunk = width
        steps = chunk / 800
        beak = 20
        x = 1
        pos = 0
        last = 60

        self.canvas.delete("all")
        while pos < chunk:
            y = float(self.data[pos]) + 0.5
            y = 120 - int((120 * y) / 1)
            self.canvas.create_line(x - 1, last, x, y, fill=col)
            last = y
            x += 1
            pos += int(steps)



class Window:
    """
    The main view, holds the tracks and the main tools
    """
    def __init__(self):
        """
        Inits the windows attributes instances and views
        """
        self.root = tk.Tk()
        self.root.geometry("1280x150")
        self.root.configure(background="black")
        self.root.title("RObin Spectrum ANalyzer - ROSAN")
        menubar = tk.Menu(self.root, bg="black", foreground='white')
        menubar.add_command(label="Add Track", command=lambda: self.add_track())
        self.root.config(menu=menubar)
        self.canvas = [None, None]
        self.zones = [None]
        self.selecting = False
        self.au_d = [None, None]
        self.tracks = [None]
        self.tracks[0] = Track(self)

    def add_track(self):
        """
        Adds a new track to the main window
        """
        self.tracks.append(Track(self))

    def selectZoneStart(self, ev, nid):
        """
        Set the start point for the sample selection
        """
        if self.tracks[nid].zone != None:
            self.tracks[nid].canvas.delete(self.tracks[nid].zone)
        print(ev, ev.x, ev.y)
        self.tracks[nid].zone = self.tracks[nid].canvas.create_rectangle(ev.x, 1,
                                                        ev.x, 120,
                                                        fill="#2453a3",
                                                        stipple="gray12")
        self.selecting = True


    def selectZoneEnd(self, ev, state, nid):
        """
        Resizes the selection
        and create the new sample when press out the click button
        """
        if state == True and self.selecting == True:
            last = self.tracks[nid].canvas.coords(self.tracks[nid].zone)
            x = last[0]
            self.tracks[nid].canvas.coords(self.tracks[nid].zone, x, 1, ev.x, 120)
        elif self.selecting == True:
            self.selecting = False
            x = self.tracks[nid].canvas.coords(self.tracks[nid].zone)[0]
            width = len(self.au_d[nid].data)
            #Scaling to view size
            x1 = int((width * x) / 1280)
            x2 = int((width * ev.x) / 1280)
            self.sample = AudioFile("samps/sample.wav")
            self.sample.data = self.au_d[nid].data[x1:x2]
            self.set_sample(self.sample.data, nid)
            print(x, ev.x)
        pass

    def set_sample(self, data, nid):
        """
        Set the sample view and instance
        """
        self.sample = Sample(self, data, nid)

    def play_file(self, event, c):
        """
        Plays the track file
        """
        if self.au_d[c] != None:
            self.au_d[c].canvas = self.tracks[c].canvas
            self.au_d[c].play()

    def open_file(self, event, c):
        """
        open a file and save data in an AudioFile object
        prints a list of files in recs/ folder
        wait for user input
        checks if file exists
        and call draw_spectrum
        """
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
            if c >= len(self.au_d):
                self.au_d.append(None)
            self.au_d[c] = AudioFile(inp)
            data = self.au_d[c].read_file(inp)
            self.draw_spectrum(data, c)
        else:
            print("No file named ", inp)
            self.open_file(event, c)

    def draw_spectrum(self, sound, c, ini=0, end=None):
        """
        Iterates the full data by steps given by chunk of data
        divided by window size
        get each value and scale each one to the track window height
        draws a line from the last to the actual
        """
        if end == None:
            end = len(sound)
        col = "#a834eb" if c == 0 else "#f2a618"
        chunk = end - ini
        steps = chunk / 1280
        beak = 20
        x = 1
        pos = 0
        last = 60
        self.tracks[c].canvas.delete("all")
        while pos < chunk and pos + ini < end:
            y = float(sound[pos + ini]) + 0.5
            y = 120 - int((120 * y) / 1)
            self.tracks[c].canvas.create_line(x - 1, last, x, y, fill=col)
            last = y
            x += 1
            pos += int(steps)

        return ini, ini + chunk

    def round_rectangle(self, x1, y1, x2, y2, s, radius=25, **kwargs):
        """
        creates a rounded rectangle shape
        used for buttons and tools
        """
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius,
                  y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius,
                  x1, y1+radius, x1, y1]
        return s.create_polygon(points, **kwargs, smooth=True)
