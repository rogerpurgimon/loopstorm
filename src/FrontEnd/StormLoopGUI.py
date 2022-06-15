#!/usr/bin/python3
# -*- encoding: latin-1 -*-

import os
import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

import threading
import atexit
import sounddevice as sd
import soundfile as sf

import essentia
from essentia.standard import *
from AudioManager import AudioManager

import numpy as np
import matplotlib.pyplot as plt

class LoopStormGUI(QMainWindow):
    loops = [[],[],[]]
    n_loops = 0 #number of loops currently in the program
    fs = 44100
    selected_loop = 0
    current_frame = 0
    

    def __init__(self):
        super().__init__()
        uic.loadUi("LoopStormInterface.ui", self)
        self.setWindowTitle("Loopstorm")
        self.importLoops.clicked.connect(lambda: self.import_loops(3))
        self.deleteLoop.clicked.connect(lambda: self.remove_loop())
        self.exportMaster.clicked.connect(lambda: self.export_master())
        self.selectMaster.clicked.connect(lambda: self.select_loop(0))
        self.selectLoop1.clicked.connect(lambda: self.select_loop(1))
        self.selectLoop2.clicked.connect(lambda: self.select_loop(2))
        self.leftArrow.clicked.connect(lambda: self.arrow("left"))
        self.rightArrow.clicked.connect(lambda: self.arrow("right"))
        self.playButton.clicked.connect(lambda: self.play_button())
        self.playButton.setCheckable(True)
        atexit.register(self.exit_handler)

    def import_loops(self, limit):
        """
        Loops only come from the loops folder. Modify that folder if we want to use different loops.
        1. Check amount of loop slots available (this should be represented in a list 	   somewhere)
        2. Check amount of loops to import in the loops folder.
        3. If not enough slots pop-up window with a warning and import amount of loops possible.
        """
        current_file_loops = []
        directory = 'loops'

        if '.DS_Store' in os.listdir(directory): # Possible bug caused by MacOS
            os.remove('loops/.DS_Store')
        # Filling an auxiliary list with all the loops in the loops file
        for filename in sorted(os.listdir(directory)):
            arg = directory + "/" + filename
            loop, fs = sf.read(arg, always_2d=True)
            if fs != 44100:
                raise ValueError("Only .wav files with 44.1k sample rate accepted")
            current_file_loops.append(loop)
        
        # Checking if there are enough available slots
        if (self.n_loops + len(current_file_loops)) > limit:
            raise ValueError("Only " + str(limit - self.n_loops) + " loop slot(s) available. Modify the loops folder.")
        else:
            for loop in current_file_loops:
                for i in range(0,3):
                    if not np.any(self.loops[i]):
                        self.loops[i] = loop
                        break


            self.n_loops += len(current_file_loops)
            print("Loops imported.")


        self.data = AudioManager(self.loops)
        self.n_loops += len(current_file_loops)
        print("Loops imported.")

        #self.represent_loops()

    def represent_loops(self):
        """
        Visually represents the loops imported.
        Return void.
        """
        i = 0
        for loop in self.loops:
            if np.any(loop):
                self.generate_image(loop, i)
            i += 1

        print("represent")
        if os.path.exists("LoopPictures/LoopPic0.png"):
            self.loop0.setPixmap(QtGui.QPixmap("LoopPictures/LoopPic0.png"))
        else:
            self.loop0.setPixmap(QtGui.QPixmap(""))
            self.loop0.setText("Master Loop")
        if os.path.exists("LoopPictures/LoopPic1.png"):
            self.loop1.setPixmap(QtGui.QPixmap("LoopPictures/LoopPic1.png"))
        else:
            self.loop1.setPixmap(QtGui.QPixmap(""))
            self.loop1.setText("Loop 1")
        if os.path.exists("LoopPictures/LoopPic2.png"):
            self.loop2.setPixmap(QtGui.QPixmap("LoopPictures/LoopPic2.png"))
        else:
            self.loop2.setPixmap(QtGui.QPixmap(""))
            self.loop2.setText("Loop 2")

    def generate_image(self, loop, i):
        """
        Generates loop pictures with indicated transients and similarities, depending on the 	 selected master loop slice.
        Return none.
        """
        time = np.linspace(0, len(loop) / self.fs, num=len(loop))

        plt.figure(i)
        plt.figure(figsize=(15, 2))
        plt.xlim([0, len(loop) / self.fs])
        plt.ylim([-1, 1])
        plt.axis('off')
        plt.plot(time, loop)
        #Draws the vertical lines
        for j in self.data.d['loop'+str(i)]['stamps']:
            plt.axvline(x=j, color='black')

        plt.savefig('LoopPictures/LoopPic' + str(i) + '.png', bbox_inches='tight')
        
    def remove_loop(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """
        self.loops[self.selected_loop] = []
        self.n_loops -= 1

        os.remove("LoopPictures/LoopPic" + str(self.selected_loop) + ".png")
        self.represent_loops()

    def export_master(self):
        """
        Exports the current master loop.
        If done more than once replaces previously exported master loops. Edit Exports file to export more than once.
        """
        sf.write('Exports/MasterLoop.wav', self.loops[0], self.fs)

    def select_loop(self, number):
        """
        """
        self.selected_loop = number
        print("Loop", self.selected_loop, "selected")

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
        # data, fs = sf.read(self.loops[0], always_2d=True)
        # current_frame = 0

        # we always assume the main loop is the main in loops[0]
        data = self.loops[self.selected_loop]
        fs = self.fs

        def callback(outdata, frames, time, status):
            # global current_frame
            if status:
                print(status)
            chunksize = min(len(data) - self.current_frame, frames)
            outdata[:chunksize] = data[self.current_frame:self.current_frame + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                self.current_frame = 0
            elif self.playButton.isChecked() == False:
                # outdata[chunksize:] = 0
                # self.current_frame = 0
                raise sd.CallbackStop()
            else:
                self.current_frame += chunksize

        stream = sd.OutputStream(
            samplerate=fs, channels=data.shape[1],
            callback=callback, finished_callback=event.set)

        if self.playButton.isChecked():
            stream.start()
            event.wait(timeout=1)
        else:
            stream.stop()


    def exit_handler(self):
        for i in range(0,3):
            if os.path.exists("LoopPictures/LoopPic" + str(i) + ".png"):
                os.remove("LoopPictures/LoopPic" + str(i) + ".png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = LoopStormGUI()
    GUI.show()
    sys.exit(app.exec_())
