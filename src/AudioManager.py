from essentia.standard import *
from AudioExtractor import AudioExtractor

class AudioManager:

    def __init(self):
        self.d = {}
        self.d['main_loop'] = {}
        self.d['main_loop']['slices'] = {}

        self.d['slave_loop'] = {}

    def __call__(self):
        print(self.d)