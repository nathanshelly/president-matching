import os
from essentia.standard import Windowing, Spectrum, MFCC, FrameGenerator
from essentia import Pool
import numpy as np

from data import load_audio

def mfcc_feature(signal):
	"""
    Cuts the signal into frames and does an MFCC of each frame,
    returning a pool holding numpy arrays of coefficient vectors 
	"""
	hann = Windowing(type = 'hann')
	spectrum = Spectrum()
	mfcc = MFCC(inputSize=513)
	
	pool = Pool()
	
	for frame in FrameGenerator(signal.astype(np.single), frameSize = 1024, hopSize = 512):
		mfcc_bands, mfcc_coeffs = mfcc(spectrum(hann(frame)))
		pool.add('mfcc_coeffs', mfcc_coeffs)
		pool.add('mfcc_bands', mfcc_bands)

    # pool currently holds mfcc_coeffs and mfcc_bands
    # as numpy arrays of coeff vectors per frame
	return pool

def mfcc_features_for_signals(signals):
    """
    Compute the MFCC feature vector for each signal
    Returns 3d numpy array of signals where each signal
    is represented as a numpy array of mfcc coefficients
    """
    return np.array([mfcc_feature(signal)['mfcc_coeffs'] for signal in signals])

def files_to_mfcc_features(dirpath):
    """
    Returns the 3d numpy array returned by mfcc_features_for_signals
    and a list of labels
    """
    signals, folders = load_audio(dirpath)
    return mfcc_features_for_signals([x[0] for x in signals]), folders

def unfold_matrix_list_with_labels(feature_matrices, labels):
    """
    Converts numpy array of signals where each signal
    is represented as a numpy array of mfcc coefficients
    into 2d vector where each value in the vector is an array of
    mfcc coefficients along with list of labels of same size, where
    each labels corresponds to the value associated with a given feature_vector
    """
    temp = [(vec, label) for vecs, label in zip(feature_matrices, labels) for vec in vecs]
    
    return map(list, zip(*temp))