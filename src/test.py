import essentia
from essentia.standard import *
import IPython.display
import matplotlib.pyplot as plt

from AudioExtractor import AudioExtractor
from AudioManager import AudioManager

if __name__ == '__main__':
    loop = MonoLoader(filename='../loops/audio1.wav')()
    loop1 = MonoLoader(filename='../loops/audio2.wav')()
    loop2 = MonoLoader(filename='../loops/audio3.wav')()
    manager = AudioManager()

    manager.add_slice(loop, 0)
    manager.add_mfccs(loop, 0)


    manager.add_slice(loop1, 1)
    manager.add_mfccs(loop1, 1)

    manager.add_slice(loop2, 2)
    manager.add_mfccs(loop2, 2)

    manager.similarity()

    print(manager.d['main_loop']['slices'][3])






