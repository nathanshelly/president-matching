import os
from essentia.standard import Windowing, Spectrum, MFCC, HighPass, LowPass
import numpy as np

from utilities import load_audio

def mfcc(frame, hopSize=512):
    """
    Compute the mfcc coefficients and band energies for a frame.
    """
    hann = Windowing(type = 'hann')
    spectrum = Spectrum()
    mfcc = MFCC(inputSize=hopSize+1)

    cs, bs = mfcc(spectrum(hann(frame)))
    # return np.concatenate((cs, bs))
    return cs

def high_pass_mfcc(frame, hopSize):
    high = HighPass()

    filtered = high(frame)

    return mfcc(filtered, hopSize)

def low_pass_mfcc(frame, hopSize):
    low  = LowPass()

    filtered = low(frame)

    return mfcc(filtered, hopSize)

def filtered_mfcc(frame, hopSize=512):
    return np.concatenate((low_pass_mfcc(frame, hopSize), high_pass_mfcc(frame, hopSize)))