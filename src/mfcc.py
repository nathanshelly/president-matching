import os
from essentia.standard import Windowing, Spectrum, MFCC
import soundfile as sf
import numpy as np

def mfcc_feature(signal):
    """Cuts the signal into frames of close to window_size, and does an MFCC of each frame
    
    NOTE: Currently treats whole signal as one frame
    """
    hann = Windowing(type = 'hann')
    spectrum = Spectrum()

	pool = essentia.Pool()

	for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
		mfcc_bands, mfcc_coeffs = mfcc(spectrum(hann(frame)))
		pool.add('lowlevel.mfcc', mfcc_coeffs)
		pool.add('lowlevel.mfcc_bands', mfcc_bands)

	return pool

def mfcc_features_for_signals(signals):
    """Compute the MFCC feature vector for each signal, and return them in a matrix"""
    return np.vstack(tuple([mfcc_feature(signal) for signal in signals]))

def load_audio(dirpath):
    files = [(os.path.join(dp, fname), os.path.basename(dp)) for dp, dn, fns in os.walk(dirpath) for fname in fns]
    return [sf.read(fname) for fname, _ in files], [folder for _, folder in files]

def files_to_mfcc_features(dirpath):
    signals, folders = load_audio(dirpath)
	# since throwing away mfccs, any reason to get them in first places?
    return mfcc_features_for_signals([x[0] for x in signals]), folders
