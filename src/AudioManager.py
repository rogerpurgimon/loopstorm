from essentia.standard import *
import numpy as np
from scipy.spatial import distance
from AudioExtractor import AudioExtractor

class AudioManager:

    def __init__(self):
        self.d = {}
        self.d['main_loop'] = {}
        self.d['main_loop']['slices'] = {}

        self.d['slave_loop1'] = {}
        self.d['slave_loop2'] = {}
        self.d['slave_loop3'] = {}
        self.d['slave_loop1']['slices'] = {}
        self.d['slave_loop2']['slices'] = {}
        self.d['slave_loop3']['slices'] = {}

    def __call__(self):
        print(self.d)

    def add_slice(self,loop,slave_idx):
        extractor_loop = AudioExtractor(loop)
        onsets_hfc = extractor_loop.get_onsets()
        extractor_loop.get_slices(onsets_hfc)

        for nslice in range(len(extractor_loop.chopList)):
            if slave_idx==1:
                self.d['slave_loop1']['slices'][nslice] = extractor_loop.chopList[nslice]

            if slave_idx==2:
                self.d['slave_loop2']['slices'][nslice] = extractor_loop.chopList[nslice]

            if slave_idx==3:
                self.d['slave_loop3']['slices'][nslice] = extractor_loop.chopList[nslice]

            if slave_idx==0:
                self.d['main_loop']['slices'][nslice] = extractor_loop.chopList[nslice]

    def add_mfccs(self,loop,slave_idx):

        extractor_loop = AudioExtractor(loop)

        if slave_idx==1:

            for nslice in range(len(self.d['slave_loop1']['slices'])):
                extractor_loop.extract_mfcc(self.d['slave_loop1']['slices'][nslice])

                self.d['slave_loop1']['slices'][nslice] = {}
                self.d['slave_loop1']['slices'][nslice]['mfccs'] = extractor_loop.mfccs[nslice]

        if slave_idx==2:
            for nslice in range(len(self.d['slave_loop2']['slices'])):
                extractor_loop.extract_mfcc(self.d['slave_loop2']['slices'][nslice])

                self.d['slave_loop2']['slices'][nslice] = {}
                self.d['slave_loop2']['slices'][nslice]['mfccs'] = extractor_loop.mfccs[nslice]

        if slave_idx==3:
            for nslice in range(len(self.d['slave_loop3']['slices'])):
                extractor_loop.extract_mfcc(self.d['slave_loop3']['slices'][nslice])

                self.d['slave_loop3']['slices'][nslice] = {}
                self.d['slave_loop3']['slices'][nslice]['mfccs'] = extractor_loop.mfccs[nslice]

        if slave_idx==0:
            for nslice in range(len(self.d['main_loop']['slices'])):
                extractor_loop.extract_mfcc(self.d['main_loop']['slices'][nslice])

                self.d['main_loop']['slices'][nslice] = {}
                self.d['main_loop']['slices'][nslice]['mfccs'] = extractor_loop.mfccs[nslice]


    def similarity(self):

        for n in range(len(self.d['main_loop']['slices'])):
            dist = np.inf
            idx = []

            #check the distances n slice --> to all slices in the slave loops
            for i in range(len(self.d['slave_loop1']['slices'])):
                new_dist = distance.euclidean(self.d['main_loop']['slices'][n]['mfccs'], self.d['slave_loop1']['slices'][i]['mfccs'])
                if new_dist < dist:
                    dist = new_dist
                    #fisrt argument reference the slave loop and the second referene the index
                    idx = ['slave_loop1',i,dist]

            for j in range(len(self.d['slave_loop2']['slices'])):
                new_dist = distance.euclidean(self.d['main_loop']['slices'][n]['mfccs'], self.d['slave_loop2']['slices'][j]['mfccs'])
                if new_dist < dist:
                    dist = new_dist
                    idx = ['slave_loop2',j,dist]

            for k in range(len(self.d['slave_loop3']['slices'])):
                new_dist = distance.euclidean(self.d['main_loop']['slices'][n]['mfccs'], self.d['slave_loop3']['slices'][k]['mfccs'])
                if new_dist < dist:
                    dist = new_dist
                    idx = ['slave_loop3',k,dist]


            #once we obtain the shortest distance we add the information to the dicctionary

            self.d['main_loop']['slices'][n]['mfccs'] = {}
            self.d['main_loop']['slices'][n]['mfccs']['similarity'] = idx




