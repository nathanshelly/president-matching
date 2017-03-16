import cPickle as pickle
import numpy as np
import collections
from scipy.io.wavfile import write
import os
import soundfile as sf

def generate_white_noise(num_samples, sample_length = 4, sample_rate = 44100):
	for i in range(num_samples):
		data = np.random.uniform(-1, 1, sample_length*sample_rate) # 44100 random samples between -1 and 1
		scaled = np.int16(data/np.max(np.abs(data)) * 32767)
		write('white_noise/white_noise_' + str(i) + '.wav', sample_rate, scaled)

def load_audio(dirpath):
    files = [(os.path.join(dp, fname), os.path.basename(dp)) for dp, dn, fns in os.walk(dirpath) for fname in fns]
    return [sf.read(fname) for fname, _ in files], [folder for _, folder in files]

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def loadFile(sFilename):
    '''Given a file name, return the contents of the file as a string'''
    f = open(sFilename, "r")
    sTxt = f.read()
    f.close()
    return sTxt

def save(data, fileName):
    pickleFile = open(fileName, 'w')
    pickle.dump(data, pickleFile)
    pickleFile.close()

def load(fileName):
    pickleFile = open(fileName, 'r')
    data = pickle.load(pickleFile)
    return data

if __name__ == '__main__':
	generate_white_noise(1000)