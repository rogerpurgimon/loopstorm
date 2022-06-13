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
        for i in range(3):
            self.d['loop'+str(i)]['loop'] = loops[i]
            self.add_onsets(loops[i],i)
            self.add_slice(loops[i],i)
            self.add_mfccs(loops[i],i)

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

    def similarity(self, mfcc1, mfcc2):
        dist = distance.euclidean(mfcc1, mfcc2)
        return dist




