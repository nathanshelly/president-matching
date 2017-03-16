import os
from essentia.standard import Windowing, Spectrum, MFCC, FrameGenerator
from essentia import Pool
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
    return np.concatenate((cs, bs))
