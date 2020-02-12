#!/usr/bin/python3
"""
Track object module
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
