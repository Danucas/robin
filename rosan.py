#!/usr/bin/python3
"""
Entry point for the Spectrum Analyser
"""

from spectrum_analyser import Window
from sound_reader import AudioFile

# Initializes the window and the main loop
win = Window()
win.root.mainloop()
