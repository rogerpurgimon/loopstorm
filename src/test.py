import essentia
from essentia.standard import *
import IPython.display
import matplotlib.pyplot as plt

from AutomaticSlicing import Slices

if __name__ == '__main__':
    loop = MonoLoader(filename='../loops/audio2.wav')()
    loop1 = Slices(loop)
    onsets_hfc = loop1.get_onsets()
    loop1.get_slices(onsets_hfc)

    # chopList contain the list of slices, separately
    print(loop1.chopList[0]) #this print the first slice


