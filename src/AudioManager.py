from essentia.standard import *
from AudioExtractor import AudioExtractor

class AudioManager:

    def __init__(self):
        self.d = {}
        self.d['main_loop'] = {}
        self.d['main_loop']['slices'] = {}

        self.d['slave_loop'] = {}

    def __call__(self):
        print(self.d)

    def add_slice(self,loop,type_loop):
        extractor_loop = AudioExtractor(loop)
        onsets_hfc = extractor_loop.get_onsets()
        extractor_loop.get_slices(onsets_hfc)

        for nslice in range(len(extractor_loop.chopList)):
            self.d[type_loop]['slices'][nslice] = extractor_loop.chopList[nslice]

    def add_mfccs(self,slice,type_loop):

        return False

    def similarity(self):
        return False
