def extract_mfcc(audio):
	audio_file = audio
	w = Windowing(type = 'blackmanharris62')
	spectrum = Spectrum()
	mfcc = essentia.standard.MFCC()
	mfccs =[]
	audio = essentia.array(audio)
	for frame in FrameGenerator(audio, frameSize = 2048 , hopSize = 1024):
		mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
		mfccs.append(mfcc_coeffs)
	mfccs = essentia.array(mfccs).T
	print("hello")
	return mfccs
