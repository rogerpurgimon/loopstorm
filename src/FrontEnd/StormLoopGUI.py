#!/usr/bin/python3
# -*- encoding: latin-1 -*-

import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

import threading
import sounddevice as sd
import soundfile as sf

import essentia
from essentia.standard import *

from AudioManager import AudioManager

import numpy as np
import matplotlib.pyplot as plt

# A venv was created in the file env in the leonardbalm file,
# this is where the pip and the python3 is located


class LoopStormGUI(QMainWindow):

    loops = []
    fs = 44100
    selected_loop = 0
    current_frame = 0
    
    def __init__(self):
        super().__init__()
        uic.loadUi("LoopStormInterface.ui", self)
        #self.loops = AudioManager()
        self.importLoops.clicked.connect(lambda: self.import_loops(self.loops, self.fs, 4))
        self.deleteLoop.clicked.connect(lambda: self.remove_loop())
        self.exportMaster.clicked.connect(lambda: self.export_master())
        self.selectMaster.clicked.connect(lambda: self.select_loop(0))
        self.selectLoop1.clicked.connect(lambda: self.select_loop(1))
        self.selectLoop2.clicked.connect(lambda: self.select_loop(2))
        self.leftArrow.clicked.connect(lambda: self.arrow("left"))
        self.rightArrow.clicked.connect(lambda: self.arrow("right"))
        self.playButton.clicked.connect(lambda: self.play_button())

    def import_loops(self, loops, fs, limit):
        """
        Loops only come from the loops folder. Modify that folder if we want to use different loops.
        1. Check amount of loop slots available (this should be represented in a list somewhere)
        2. Check amount of loops to import in the loops folder.
        3. If not enough slots pop-up window with a warning and import amount of loops possible.
        """
        current_file_loops = []
        #sampling_rates = []
        directory = 'loops'

        # Filling an auxiliary list with all the loops in the loops file
        for filename in os.listdir(directory):
            arg = directory + "/" + filename
            loop, fs = sf.read(arg, always_2d=True)
            #loop = MonoLoader(filename=arg)
            current_file_loops.append(loop)
            #sampling_rates.append(fs)

        # Checking if there are enough available slots
        if len(loops) + len(current_file_loops) > limit:
            raise ValueError("Not enough slots available! Remove some loops from LoopStorm or from the loops folder.")
        else:
            self.loops = current_file_loops
            #self.fs = sampling_rates
            print("Loops compilats")    
                 
        
        self.represent_loops()

    def represent_loops(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """
        i = 0
        for loop in self.loops:
            self.generate_image(loop, i)
            i += 1
    
    def generate_image(self, loop, i):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """
        time = np.linspace(0, len(loop) / self.fs, num=len(loop))

        plt.figure(1)
        plt.figure(figsize=(15, 2))
        plt.axis('off')
        plt.plot(time, loop)
        plt.savefig('LoopPictures/LoopPic' + str(i) + '.png')

    def remove_loop(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """
        self.loops.pop(self.selected_loop)
        

    def export_master(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """

    def select_loop(self, number):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """
        self.selected_loop = number
        print("loop", self.selected_loop, "seleccionat")
        

    def arrow(self, direction):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """

    def play_button(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """
        event = threading.Event()
        #data, fs = sf.read(self.loops[0], always_2d=True)
        #current_frame = 0
        
        #we always assume the main loop is the main in loops[0]
        data = self.loops[self.selected_loop]
        fs = self.fs
        
        def callback(outdata, frames, time, status):
            #global current_frame 	
            if status:
                print(status)
            chunksize = min(len(data) - self.current_frame, frames)
            outdata[:chunksize] = data[self.current_frame:self.current_frame + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                self.current_frame = 0            		
		#raise sd.CallbackStop()
            else:
                self.current_frame += chunksize

        stream = sd.OutputStream(
            samplerate=fs, channels=data.shape[1],
            callback=callback, finished_callback=event.set)
	
        with stream:
            event.wait()  # Wait until playback is finished


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = LoopStormGUI()
    GUI.show()
    sys.exit(app.exec_())
