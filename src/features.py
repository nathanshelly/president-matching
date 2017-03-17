from essentia.standard import Windowing, FrameGenerator
from essentia import Pool

import numpy as np

from utilities import load_audio
from mfcc import mfcc

def compute_features(signal, features=[mfcc]):
    """Compute features frame-by-frame on a signal.
    
    Features is a list of functions for generating features."""

    pool = Pool()

    for frame in FrameGenerator(signal.astype(np.single), frameSize = 1024, hopSize = 512):
        feature_vec = np.array([], dtype=np.single)
        for func in features:
            feature_vec = np.concatenate((feature_vec, func(frame)))
        
        pool.add("features", feature_vec)

    # pool currently holds mfcc_coeffs and mfcc_bands
    # as numpy arrays of coeff vectors per frame
    return pool

def features_for_signals(signals, features):
    """
    Compute the MFCC feature vector for each signal
    Returns 3d numpy array of signals where each signal
    is represented as a numpy array of mfcc coefficients
    """
    return np.array([compute_features(signal, features)["features"] for signal in signals])

def files_to_features(dirpath, features=[mfcc]):
    """
    Returns the 3d numpy array returned by mfcc_features_for_signals
    and a list of labels
    """
    signals, folders = load_audio(dirpath)
    return features_for_signals([x[0] for x in signals], features), folders

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

def knn_train_features(dirpath, features=[mfcc]):
    signal_features, signal_labels = files_to_features(dirpath, features)
    return unfold_matrix_list_with_labels(signal_features, signal_labels)

if __name__ == "__main__":
    pass
