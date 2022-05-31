import essentia
from essentia.standard import *
import IPython.display
import matplotlib.pyplot as plt

from AudioExtractor import AudioExtractor
from AudioManager import AudioManager

if __name__ == '__main__':
    loop = MonoLoader(filename='../loops/audio2.wav')()
    manager = AudioManager()
    manager.add_slice(loop,0)
    manager.add_mfccs(loop,0)

    print(manager.d['main_loop']['slices'][1]['mfccs'])




