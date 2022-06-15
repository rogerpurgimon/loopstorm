import essentia
import numpy as np
from essentia.standard import *

class AudioExtractor:

    def __init__(self,loop):
        self.loop = loop
        self.chopList = []
        self.fs = 44100
        self.w_onset = 'hann'
        self.mfccs = []
        self.w_mfcc = 'blackmanharris62'

    def __call__(self):
        return self.chopList

    def get_onsets(self):
        od = OnsetDetection(method='hfc')

        w = Windowing(type=self.w_onset)
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


    def extract_mfcc(self,slice):
        w = Windowing(type=self.w_mfcc)
        spectrum = Spectrum()
        mfcc = MFCC()
        mfcc_sin = []
        for frame in FrameGenerator(slice, frameSize=2048, hopSize=1024):
            mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
            mfcc_sin.append(mfcc_coeffs)
        mfcc_sin = essentia.array(mfcc_sin).T
        #mfcc_sin = np.mean(mfcc_sin,axis=1) #mean for columns
        mfcc_sin = np.concatenate(mfcc_sin, axis=0)
        self.mfccs.append(mfcc_sin)
