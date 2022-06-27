import os
import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

import threading
import atexit
import sounddevice as sd
import soundfile as sf

from math import dist 
import librosa as lb
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance as dis


class LoopStorm(QMainWindow):
    stereo_loops = []
    d = {'loop0': {}, 'loop1': {}, 'loop2': {}, 'slices': []}

    n_loops = 0  # number of loops currently in the program
    sr = 44100  # Sample frequency
    selected_loop = 0  # Currently selected loop (0: master, 1:slave loop 1, 2:slave loop 2)
    current_frame = 0  # Used in play button

    def __init__(self):
        super().__init__()
        uic.loadUi("LoopStormInterface.ui", self)
        self.setWindowTitle("Loopstorm")
        self.empty_dictionaries()
        self.importLoops.clicked.connect(lambda: self.import_loops())
        self.deleteLoop.clicked.connect(lambda: self.remove_loop())
        self.exportMaster.clicked.connect(lambda: self.export_master())
        self.selectMaster.clicked.connect(lambda: self.select_loop(0))
        self.selectLoop1.clicked.connect(lambda: self.select_loop(1))
        self.selectLoop2.clicked.connect(lambda: self.select_loop(2))
        self.leftArrow.clicked.connect(lambda: self.master_arrow("left"))
        self.rightArrow.clicked.connect(lambda: self.master_arrow("right"))
        self.leftArrow_2.clicked.connect(lambda: self.slave_arrow("left"))
        self.rightArrow_2.clicked.connect(lambda: self.slave_arrow("right"))
        self.replace.clicked.connect(lambda: self.replaceF(False))
        self.putBack.clicked.connect(lambda: self.replaceF(True))
        self.playButton.clicked.connect(lambda: self.play_button())
        self.playButton.setCheckable(True)
        atexit.register(self.exit_handler)

    def import_loops(self):
        """
        Import .wav files into LoopStorm.
        Loops only come from the loops folder. Modify that folder if you want to use different loops.
        """
        limit = 3
        aux_loops = []
        aux_time_onsets = []
        aux_index_onsets = []

        if '.DS_Store' in os.listdir('loops'):  # Possible bug caused by MacOS
            os.remove('loops/.DS_Store')
        # Filling auxiliary lists with all the loops, time and sample indices
        for filename in sorted(os.listdir('loops')):
            arg = "loops/" + filename
            y, sr = lb.load(arg, sr=None)  # Librosa works with the audio in mono
            onset_t = lb.onset.onset_detect(y=y, sr=sr, units='time', hop_length=32)
            onset_idx = lb.onset.onset_detect(y=y, sr=sr, units='samples', hop_length=32)
            loop, fs = sf.read(arg, always_2d=True)  # Also storing the audio in stereo for the play button
            if sr != 44100:
                raise ValueError("Only .wav files with 44.1k sample rate accepted")
            aux_loops.append(y)
            aux_time_onsets.append(onset_t)
            aux_index_onsets.append(onset_idx)
            self.stereo_loops.append(loop)

        # Checking if there are enough available slots
        if (self.n_loops + len(aux_loops)) > limit:
            raise ValueError("Only " + str(limit - self.n_loops) + " loop slot(s) available. Modify the loops folder.")
        else:  # Filling dictionary with the auxiliary lists
            for loop, onset_t, onset_idx in zip(aux_loops, aux_time_onsets, aux_index_onsets):
                for i in range(3):
                    if not np.any(self.d['loop' + str(i)]['loop']):
                        self.d['loop' + str(i)]['loop'] = loop
                        self.d['loop' + str(i)]['stamps'] = onset_t
                        self.d['loop' + str(i)]['indices'] = onset_idx
                        break
            self.n_loops += len(aux_loops)
            print("Loops imported.")

        # Computing slices mfcc similarities
        self.compute_similarities()

        # Generating the images
        for i in range(3):
            if np.any(self.d['loop' + str(i)]['loop']):
                self.generate_image(i, 0)

        # Representing the images
        self.represent_loops()

    def compute_similarities(self):
        """
        Computes similarities between the current master slice selected and all the slices from the slave loops.
        Uses mfcc for comparison.
        """
        mfccs = {'mfcc0': [], 'mfcc1': [], 'mfcc2': []}
        
        #print(mfccs['mfcc0'])
        # Emptying similarities
        for i in range(1,3):
            self.d['loop'+str(i)]['similarity'] = np.array([])

        # Get mfccs
        for i in range(3):
            for j in range(self.d['loop'+str(i)]['indices'].size-1):
                min_frame = self.d['loop'+str(i)]['indices'][j]
                max_frame = self.d['loop'+str(i)]['indices'][j+1]
                mfcc = lb.feature.mfcc(y=self.d['loop' + str(i)]['loop'][min_frame:max_frame], sr=self.sr, n_mfcc=12)
                mfcc_reduct = np.mean(mfcc, axis=1)
                mfccs['mfcc'+str(i)].append(mfcc_reduct)

        # Compute similarities
        for i in range(1,3):
            for j in range(np.shape(mfccs['mfcc'+str(i)])[0]):
                current_mfcc = mfccs['mfcc' + str(i)][j]
                distance = dist(mfccs['mfcc0'][self.d['slices'][0]], current_mfcc)
                #print(mfccs['mfcc0'][self.d['slices'][0]])
                self.d['loop'+str(i)]['similarity'] = np.append(self.d['loop'+str(i)]['similarity'], distance)

        # Normalize similarities
        conc = np.concatenate((self.d['loop1']['similarity'], self.d['loop2']['similarity']))
        self.d['loop1']['similarity'] = (self.d['loop1']['similarity'] - min(conc)) / (max(conc) - min(conc))
        self.d['loop2']['similarity'] = (self.d['loop2']['similarity'] - min(conc)) / (max(conc) - min(conc))
        # print(self.d['loop1']['similarity'])
        
    def generate_image(self, i, position):
        """
        Receives an index i representing the corresponding loop and the slice position of the current slice selected.
        Generates loop pictures and saves in the LoopPictures folder.
        """
        loop = self.d['loop'+str(i)]['loop']
        total_time = len(loop) / self.sr

        # Plot and colors
        plt.figure(figsize=(15, 2))
        plt.axis('off')
        plt.xlim([0, total_time])
        plt.ylim([-1, 1])
        if i in range(1, 3):
            for j in range(self.d['loop' + str(i)]['similarity'].size-1):
                xmin = self.d['loop' + str(i)]['stamps'][j]
                xmax = self.d['loop' + str(i)]['stamps'][j + 1]
                loopmin = self.d['loop' + str(i)]['indices'][j]
                loopmax = self.d['loop' + str(i)]['indices'][j+1]
                section_time = np.linspace(xmin, xmax, num=len(loop[loopmin:loopmax]))
                plt.plot(section_time, loop[loopmin:loopmax], color=self.get_color(self.d['loop' + str(i)]['similarity'][j]))
        else:
            time = np.linspace(0, total_time, num=len(loop))
            plt.plot(time, loop)

        # Vertical lines
        for j in self.d['loop' + str(i)]['stamps']:
            plt.axvline(x=j, color='black')
        plt.axvline(x=total_time, color='black')  # last line

        # Horizontal lines
        minlim =self.d['loop' + str(i)]['stamps'][position] / total_time
        if (position + 1) == (len(self.d['loop'+str(i)]['stamps'])):
            maxlim = total_time
        else:
            maxlim = self.d['loop' + str(i)]['stamps'][position+1] / total_time

        plt.axhline(y=0.97, color='black', xmin = minlim, xmax = maxlim)
        plt.axhline(y=-0.97, color='black', xmin = minlim, xmax = maxlim)

        # Saves plot
        plt.savefig('LoopPictures/LoopPic' + str(i) + '.png', bbox_inches='tight')
        plt.close()  # Close figure to save memory

    def get_color(self, similarity):
        """
        Receives a similarity value and returns its correspondent color.
        """
        if similarity>=0 and similarity<0.2:
            return 'aqua'
        elif similarity>0.2 and similarity<0.4:
            return 'aquamarine'
        elif similarity>0.4 and similarity<0.6:
            return 'beige'
        elif similarity>0.6 and similarity<0.8:
            return 'red'
        elif similarity>0.8 and similarity<=1:
            return 'crimson'
        else:
            return 'black'

    def represent_loops(self):
        """
        Checks the images generated in the folder LoopPictures and loads them in the interface.
        Return void.
        """
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

    def remove_loop(self):
        """
        Resets the selected loop to an empty list and removes its correspondent picture from the folder LoopPictures.
        """
        self.d['loop' + str(self.selected_loop)]['loop'] = []
        self.n_loops -= 1

        os.remove("LoopPictures/LoopPic" + str(self.selected_loop) + ".png")
        self.represent_loops()

    def export_master(self):
        """
        Exports the current master loop.
        If done more than once replaces previously exported master loops. Edit Exports files to export more than once.
        """
        sf.write('Exports/MasterLoop.wav', self.d['loop0']['loop'], self.sr)

    def select_loop(self, number):
        """
        Sets a given loop as selected.
        """
        self.selected_loop = number
        self.generate_image(self.selected_loop, self.d['slices'][self.selected_loop])

        print("Loop", self.selected_loop, "selected")
        self.represent_loops()

    def master_arrow(self, direction):
        """
        """
        if direction == 'right':
            if (self.d['slices'][0] +1) >= len(self.d['loop0']['stamps']):
                return
            else:
                self.d['slices'][0] += 1
        elif direction == 'left':
            if (self.d['slices'][0]-1) < 0:
                return
            else:
                self.d['slices'][0] -= 1

        self.compute_similarities()
        
        self.generate_image(0, self.d['slices'][0]) # Representing selected slice of master loop
        # Updating colors of slaves
        self.generate_image(1, self.d['slices'][1])
        self.generate_image(2, self.d['slices'][2])
        
        self.represent_loops()

    def slave_arrow(self, direction):
        """
        """
        if self.selected_loop == 0:
            return

        if direction == 'right':
            if (self.d['slices'][self.selected_loop] +1) >= len(self.d['loop' + str(self.selected_loop)]['stamps']):
                return
            else:
                self.d['slices'][self.selected_loop] += 1
        elif direction == 'left':
            if (self.d['slices'][self.selected_loop]-1) < 0:
                return
            else:
                self.d['slices'][self.selected_loop] -= 1

        self.generate_image(self.selected_loop, self.d['slices'][self.selected_loop])
        self.represent_loops()
        
    def replaceF(self, put_back):
        """
            Modify the master loop in the loops folder and import loops again.
            The put back button only works for the last replaced slice.
        """
        if self.selected_loop == 0:
            return
        
        # We define the min and max limits for the chop (if statement to deal with the last slice) of the slave loop
        if (self.d['slices'][self.selected_loop] == len(self.d['loop'+str(self.selected_loop)]['indices'])): # Checks if the current selected slave slice is the last
            slv_minbound = self.d['loop'+str(self.selected_loop)]['indices'][self.d['slices'][self.selected_loop]]
            slv_maxbound = len(self.d['loop'+str(self.selected_loop)]['loop'])
        else:
            slv_minbound = self.d['loop'+str(self.selected_loop)]['indices'][self.d['slices'][self.selected_loop]]
            slv_maxbound = self.d['loop'+str(self.selected_loop)]['indices'][self.d['slices'][self.selected_loop]+1]
            
        # We store the slave slice in a variable
        slv_slice = self.d['loop'+str(self.selected_loop)]['loop'][slv_minbound:slv_maxbound]

        # We define the min and max limits for the chop (if statement to deal with the last slice) of the master loop
        if (self.d['slices'][0] == len(self.d['loop0']['indices'])): # Checks if the current selected master slice is the last
            mas_minbound = self.d['loop0']['indices'][self.d['slices'][0]]
            mas_maxbound = len(self.d['loop0']['loop'])
        else:
            mas_minbound = self.d['loop0']['indices'][self.d['slices'][0]]
            mas_maxbound = self.d['loop0']['indices'][self.d['slices'][0]+1]
        
        # We store the master sections (before and after the replaced slice)
        mas_part1 = self.d['loop0']['loop'][0:mas_minbound]
        mas_part2 = self.d['loop0']['loop'][mas_maxbound:len(self.d['loop0']['loop'])]
        
        if (put_back == False):
            sf.write('SavedMaster/MasterLoop.wav', self.d['loop0']['loop'], self.sr) # Saving the current master loop
            self.d['loop0']['loop'] = np.concatenate((mas_part1, slv_slice, mas_part2)) # We alter the master loop concatenating the three sections sliced
        else:
            y, sr = lb.load('SavedMaster/MasterLoop.wav', sr=None) # Recovering previous master loop
            self.d['loop0']['loop'] = y # We alter the master loop back to the unaltered version
            
        # Overwriting the audio file
        sf.write('loops/audio1.wav', self.d['loop0']['loop'], self.sr)
        
        # Emptying program and importing back
        self.empty_dictionaries()
        self.n_loops = 0
        self.import_loops()
        
    def empty_dictionaries(self):
        """
        Initializes empty dictionary
        """
        for i in range(3):
            self.d['loop'+str(i)]['loop'] = np.array([])  # Entire loops
            self.d['loop'+str(i)]['stamps'] = np.array([])  # Times of the onset values
            self.d['loop' + str(i)]['indices'] = np.array([])  # Sample indices of the onset values

        for i in range(1, 3):
            self.d['loop'+str(i)]['similarity'] = np.array([]) # Similarities of the slave loops current slices to the master current slice
        
        self.d['slices'] = [0,0,0]
        
    def play_button(self):
        """
        Plays selected loop
        """
        event = threading.Event()
        # data, fs = sf.read(self.loops[0], always_2d=True)
        # current_frame = 0

        # we always assume the main loop is the main in loops[0]
        data = self.stereo_loops[self.selected_loop]
        fs = self.sr

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
        for i in range(0, 3):
            if os.path.exists("LoopPictures/LoopPic" + str(i) + ".png"):
                os.remove("LoopPictures/LoopPic" + str(i) + ".png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = LoopStorm()
    GUI.show()
    sys.exit(app.exec_())
