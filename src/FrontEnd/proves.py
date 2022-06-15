import os
import sys
import threading
import atexit
import sounddevice as sd
import soundfile as sf

import essentia
from essentia.standard import *
from AudioManager import AudioManager

import numpy as np
import matplotlib.pyplot as plt

current_file_loops = []
directory = 'loops'

loops = [[],[],[]]
n_loops = 0 #number of loops currently in the program


if '.DS_Store' in os.listdir(directory): # Possible bug caused by MacOS
    os.remove('loops/.DS_Store')
# Filling an auxiliary list with all the loops in the loops file
for filename in sorted(os.listdir(directory)):
    arg = directory + "/" + filename
    loop, fs = sf.read(arg, always_2d=True)
    if fs != 44100:
        raise ValueError("Only .wav files with 44.1k sample rate accepted")
    current_file_loops.append(loop)
print("loops dins current_file_loops")

# Checking if there are enough available slots
if (n_loops + len(current_file_loops)) > 3:
    raise ValueError("Only " + str(limit - n_loops) + " loop slot(s) available. Modify the loops folder.")
else:
    for loop in current_file_loops:
        for i in range(0,3):
            if not np.any(loops[i]):
                loops[i] = loop
                break
  
print(loops[0].sum(axis=1))

n_loops += len(current_file_loops)
print("Loops imported.")



