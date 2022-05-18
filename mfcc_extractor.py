import essentia
import essentia.standard as es
import essentia.streaming as ess
#import matplotlib.pyplot as plt
#from pathlib import Path
import time


def extract_mfcc(audio):
	
	#script_dir = Path().resolve()
	audio_file = audio
	#audio_file = "audio1.wav"
	start_time = time.time()

	audio = es.MonoLoader(filename=str(audio_file))()
	w = es.Windowing(type = 'blackmanharris62')
	spectrum = es.Spectrum()
	mfcc = es.MFCC()
	mfccs =[]
		
	for frame in es.FrameGenerator(audio, frameSize = 2048 , hopSize = 1024):
		mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
		mfccs.append(mfcc_coeffs)
	mfccs = essentia.array(mfccs).T
	#print(mfccs)
	return mfccs
