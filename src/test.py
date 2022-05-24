import essentia
from essentia.standard import *
import IPython.display
import matplotlib.pyplot as plt

from AutomaticSlicing import Slices
from mfcc_extractor import *

if __name__ == '__main__':
    loop = MonoLoader(filename='../loops/audio2.wav')()
    loop1 = Slices(loop)
    onsets_hfc = loop1.get_onsets()
    loop1.get_slices(onsets_hfc)

    # chopList contain the list of slices, separately
    print(loop1.chopList[0]) #this print the first slice
    
    mfccs = extract_mfcc(loop1.chopList[0])
    print("The mfccs of the first slice are:", mfccs)


