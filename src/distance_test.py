import essentia
from essentia.standard import *
import IPython.display
import matplotlib.pyplot as plt
from scipy.spatial import distance	# import to have euclidean distance


from AudioExtractor import AudioExtractor
from mfcc_extractor import *

if __name__ == '__main__':
    loop = MonoLoader(filename='../loops/audio2.wav')()
    loop1 = AudioExtractor(loop)
    onsets_hfc = loop1.get_onsets()
    loop1.get_slices(onsets_hfc)

    # chopList contain the list of slices, separately
    #loop_slices = []
    #for i in range(10):
    slice = loop1.chopList[0]
    loop1.extract_mfcc(slice) 
    #loop_slices.append(loop1.mfccs) 
    
    d1 = distance.euclidean(loop1.mfccs[0], loop1.mfccs[1])
    d2 = distance.euclidean(loop1.mfccs[0], loop1.mfccs[2])
    
    print("Which slice is more similar to slice 0?")
    if d1 > d2:
    	print("2 is more similar")
    else:
    	print("1 is more similar")


