import os
import essentia.standard
import scipy.io.wavfile as wav
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def mfcc_feature(signal, approx_window_size=2048):
    """Cuts the signal into frames of close to window_size, and does an MFCC of each frame
    
    NOTE: Currently treats whole signal as one frame
    """
    hann = essentia.standard.Windowing()
    spectrum = essentia.standard.Spectrum()
    spec = spectrum(hann(signal.astype(np.single)))
    mfcc = essentia.standard.MFCC(inputSize=len(spec))

    bands, mfccs = mfcc(spec)

    return np.concatenate((bands, mfccs))

def mfcc_features_for_signals(signals, approx_window_size=2048):
    """Compute the MFCC feature vector for each signal, and return them in a matrix"""
    return np.vstack(tuple([mfcc_feature(signal, approx_window_size) for signal in signals]))

def load_audio(dirpath):
    files = [os.path.join(dp, fname) for dp, dn, fns in os.walk(dirpath) for fname in fns]
    return [wav.read(fname) for fname in files]

def files_to_mfcc_features(dirpath):
    signals = load_audio(dirpath)
    return mfcc_features_for_signals([x[1] for x in signals])

def train_knn(data, labels, n_neighbors=5):
    """Train and return a KNN model"""
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(data, labels)
    return clf

def test_knn(knn_classifier, data):
    return knn_classifier.predict(data)
