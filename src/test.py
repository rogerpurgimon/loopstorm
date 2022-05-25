import essentia
from essentia.standard import *
import IPython.display
import matplotlib.pyplot as plt

from AudioExtractor import AudioExtractor
from mfcc_extractor import *

if __name__ == '__main__':
    loop = MonoLoader(filename='../loops/audio2.wav')()
    loop1 = AudioExtractor(loop)
    onsets_hfc = loop1.get_onsets()
    loop1.get_slices(onsets_hfc)

    # chopList contain the list of slices, separately
    slice = loop1.chopList[0] #first slice


    loop1.extract_mfcc(slice)
    print("The mfccs of the first slice are:", loop1.mfccs)


