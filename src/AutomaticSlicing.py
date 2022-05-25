import essentia
import numpy as np
from essentia.standard import *
import IPython
from scipy.io import wavfile
import matplotlib.pyplot as plt

class Slices:

    def __init__(self,loop):
        self.loop = loop
        self.chopList = []
        self.fs = 44100
        self.w = 'hann'

    def __call__(self):
        return self.chopList

    def get_onsets(self):
        od = OnsetDetection(method='hfc')

        w = Windowing(type=self.w)
        fft = FFT()  # this gives us a complex FFT
        c2p = CartesianToPolar()  # and this turns it into a pair (magnitude, phase)
        pool = essentia.Pool()

        # Computing onset detection functions.
        for frame in FrameGenerator(self.loop, frameSize=1024, hopSize=512):
            mag, phase, = c2p(fft(w(frame)))
            pool.add('features.hfc', od(mag, phase))

        onsets = Onsets()
        onsets_hfc_seconds = onsets(essentia.array([pool['features.hfc']]), [1])

        onsets_hfc_samples = onsets_hfc_seconds * self.fs #retun
        return onsets_hfc_samples, onsets_hfc_seconds


    def get_slices(self,onsets_hfc):
        onsets_hfc = onsets_hfc[0]  # onset stamps in samples
        for onset in range(len(onsets_hfc) - 1):
            self.chopList.append(self.loop[int(onsets_hfc[onset]):int((onsets_hfc[onset + 1]))])





