import numpy as np

from essentia.standard import Chromagram

def chromagram(signal):
    chrom = Chromagram()

    return chrom(signal.astype(np.complex64))