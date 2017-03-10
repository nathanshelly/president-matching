import os
from essentia.standard import Windowing, Spectrum, MFCC, FrameGenerator
from essentia import Pool
import soundfile as sf
import numpy as np

def mfcc_feature(signal):
	"""Cuts the signal into frames of close to window_size, and does an MFCC of each frame
	NOTE: Currently treats whole signal as one frame
	"""
	hann = Windowing(type = 'hann')
	spectrum = Spectrum()
	mfcc = MFCC(inputSize=513)
	
	pool = Pool()
	
	for frame in FrameGenerator(signal.astype(np.single), frameSize = 1024, hopSize = 512):
		mfcc_bands, mfcc_coeffs = mfcc(spectrum(hann(frame)))
		pool.add('mfcc_coeffs', mfcc_coeffs)
		pool.add('mfcc_bands', mfcc_bands)

	# print pool['mfcc_coeffs'].shape
	# print pool['mfcc_bands'].shape

	return pool

def mfcc_features_for_signals(signals):
    """Compute the MFCC feature vector for each signal, and return them in a matrix"""
    return np.array([mfcc_feature(signal)['mfcc_coeffs'] for signal in signals])

def load_audio(dirpath):
    files = [(os.path.join(dp, fname), os.path.basename(dp)) for dp, dn, fns in os.walk(dirpath) for fname in fns]
    return [sf.read(fname) for fname, _ in files], [folder for _, folder in files]

def files_to_mfcc_features(dirpath):
    signals, folders = load_audio(dirpath)
	# since throwing away mfccs, any reason to get them in first places?
    return mfcc_features_for_signals([x[0] for x in signals]), folders

def unfold_matrix_list_with_labels(feature_matrices, labels):
    print feature_matrices.shape

    temp = [(vec, label) for vecs, label in zip(feature_matrices, labels) for vec in vecs]
    
    return map(list, zip(*temp))