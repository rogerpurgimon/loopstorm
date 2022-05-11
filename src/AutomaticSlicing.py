import essentia
from essentia.standard import *
import IPython
from scipy.io import wavfile
import matplotlib.pyplot as plt

class AutomaticSlicing:

    def get_onsets_hfc(audio,fs):
        od = OnsetDetection(method='hfc')

        w = Windowing(type='hann')
        fft = FFT()  # this gives us a complex FFT
        c2p = CartesianToPolar()  # and this turns it into a pair (magnitude, phase)
        pool = essentia.Pool()

        # Computing onset detection functions.
        for frame in FrameGenerator(audio, frameSize=1024, hopSize=512):
            mag, phase, = c2p(fft(w(frame)))
            pool.add('features.hfc', od(mag, phase))

            onsets = Onsets()
            onsets_hfc_seconds = onsets(essentia.array([pool['features.hfc']]), [1])

        onsets_hfc_samples = onsets_hfc_seconds * fs #retun
        return onsets_hfc_samples, onsets_hfc_seconds


    def get_slices(audio, fs):
        onsets_hfc = get_onsets_hfc(audio,fs)[0]
        chopList = []
        for onset in range(len(onsets_hfc) - 1):
            chopList.append(audio[int(onsets_hfc[onset]):int((onsets_hfc[onset + 1]))])

        return chopList


