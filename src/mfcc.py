import os
import essentia.standard
import soundfile as sf
import numpy as np

def mfcc_feature(signal):
    """Cuts the signal into frames of close to window_size, and does an MFCC of each frame
    
    NOTE: Currently treats whole signal as one frame
    """
    hann = essentia.standard.Windowing()
    spectrum = essentia.standard.Spectrum()
    window = hann(signal.astype(np.single))
    if window.size % 2 != 0:
        window = window[:window.size - 1]
    spec = spectrum(window)
    mfcc = essentia.standard.MFCC(inputSize=len(spec))

    bands, mfccs = mfcc(spec)

    return np.concatenate((bands, mfccs))

def mfcc_features_for_signals(signals):
    """Compute the MFCC feature vector for each signal, and return them in a matrix"""
    return np.vstack(tuple([mfcc_feature(signal) for signal in signals]))

def load_audio(dirpath):
    files = [(os.path.join(dp, fname), os.path.basename(dp)) for dp, dn, fns in os.walk(dirpath) for fname in fns]
    return [sf.read(fname) for fname, _ in files], [folder for _, folder in files]

def files_to_mfcc_features(dirpath):
    signals, folders = load_audio(dirpath)
    return mfcc_features_for_signals([x[0] for x in signals]), folders
