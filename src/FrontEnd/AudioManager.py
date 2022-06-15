from essentia.standard import *
import numpy as np
from scipy.spatial import distance
from AudioExtractor import AudioExtractor

class AudioManager:
    d = {}
    d['loop0'] = {}
    d['loop1'] = {}
    d['loop2'] = {}

    d['loop0']['loop'] = []
    d['loop1']['loop'] = []
    d['loop2']['loop'] = []

    d['loop0']['stamps'] = []
    d['loop1']['stamps'] = []
    d['loop2']['stamps'] = []

    d['loop0']['slices'] = [[],[]]
    d['loop1']['slices'] = [[],[]]
    d['loop2']['slices'] = [[],[]]


    def __init__(self, loops):
        self.max_l = 0
        for i in range(3):
            self.d['loop'+str(i)]['loop'] = loops[i]
            self.add_onsets(loops[i],i)
            self.add_slice(loops[i],i)
            self.add_mfccs(loops[i],i)
        self.max_length()

    def __call__(self):
        print(self.d)

    def add_onsets(self, loop, slave_idx):
        extractor_loop = AudioExtractor(loop)
        onsets_hfc = extractor_loop.get_onsets()

        for i in range(3):
           self.d['loop'+str(i)]['stamps'] = onsets_hfc[1]

    def add_slice(self,loop,slave_idx):
        extractor_loop = AudioExtractor(loop)
        onsets_hfc = extractor_loop.get_onsets()
        extractor_loop.get_slices(onsets_hfc)

        for i in range(3):
            self.d['loop'+ str(i)]['slices'][0] = extractor_loop.chopList

    def add_mfccs(self,loop,slave_idx):

        extractor_loop = AudioExtractor(loop)
        for i in range(3):
            for nslice in range(len(self.d['loop'+ str(i)]['slices'][0])):
                extractor_loop.extract_mfcc(self.d['loop'+ str(i)]['slices'][0][nslice])
                self.d['loop'+ str(i)]['slices'][1].append(extractor_loop.mfccs[nslice])
    def max_length(self):
        # zero padding
        max = 0
        for n in range(len(self.d['loop0']['slices'][1])):
            current_len = len(self.d['loop0']['slices'][1][n])
            if current_len > max:
                max = current_len

        for n in range(len(self.d['loop1']['slices'][1])):
            current_len = len(self.d['loop1']['slices'][1][n])
            if current_len > max:
                max = current_len

        for n in range(len(self.d['loop2']['slices'][1])):
            current_len = len(self.d['loop2']['slices'][1][n])
            if current_len > max:
                max = current_len

        self.max_l = max
        print(max)

    def similarity(self, mfcc1, mfcc2):

        # add zeros at the end of the mfccs.
        aux1 = np.zeros(self.max_l)
        aux1[0:len(mfcc1)] = mfcc1
        mfcc1 = aux1

        aux2 = np.zeros(self.max_l)
        aux2[0:len(mfcc2)] = mfcc2
        mfcc2 = aux2

        dist = distance.euclidean(mfcc1, mfcc2)

        return dist




