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
    mfcc = essentia.standard.MFCC()

    # n_frames = len(signal) / approx_window_size + 1
    # frames = np.array_split(signal, n_frames)
    # bands, mfccs = map(list, zip(*[mfcc(spectrum(hann(frame.astype(np.single)))) for frame in frames]))
    bands, mfccs = mfcc(spectrum(hann(signal.astype(np.single))))

    return np.concatenate((bands, mfccs))

def mfcc_features_for_signals(signals, approx_window_size=2048):
    """Compute the MFCC feature vector for each signal, and return them in a matrix"""
    return np.vstack(tuple([mfcc_feature(signal, approx_window_size) for signal in signals]))

def load_audio(dirpath):
    files = [os.path.join(dp, fname) for dp, dn, fns in os.walk(dirpath) for fname in fns]
    return [wav.read(fname) for fname in files]

def train_knn(data, labels, n_neighbors=5):
    """Train and return a KNN model"""
    assert(data.shape[0] == labels.shape[0], "Number of training examples and labels mismatched")
    
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(data, labels)
    return clf

def files_to_mfcc_features(dirpath):
    signals = load_audio(dirpath)
    return mfcc_features_for_signals([x[1] for x in signals])

def test_knn(knn_classifier, data):
    return knn_classifier.predict(data)

if __name__ == "__main__":
    voice_features = files_to_mfcc_features('an4/wav/an4_clstk')
    voice_labels = ["voice"] * voice_features.shape[0]

    white_noise_features = files_to_mfcc_features('white_noise/train')
    white_noise_labels = ["white_noise"] * white_noise_features.shape[0]

    print "Features computed, beginning training...."

    all_features = np.vstack((white_noise_features, voice_features))
    all_labels = np.concatenate((white_noise_labels, voice_labels))
    clf = train_knn(all_features, all_labels)

    print "Training completed, testing..."

    white_noise_tests = files_to_mfcc_features('white_noise/test')
    voice_tests = files_to_mfcc_features('an4/wav/an4test_clstk')

    print "White noise test:", test_knn(clf, white_noise_tests)
    print "Voice test:", test_knn(clf, voice_tests)



