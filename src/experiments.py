import numpy as np
from mfcc_knn import files_to_mfcc_features, train_knn, test_knn

def experiment1(n_neighbors=5):
    """Train a knn model on ~1000 white noise and ~1000 voice snippets.
    Test with ~20 held out white noise and voice snippets, all of which are
    classified correctly.
    """
    voice_features = files_to_mfcc_features('an4/wav/an4_clstk')
    voice_labels = ["voice"] * voice_features.shape[0]

    white_noise_features = files_to_mfcc_features('white_noise/train')
    white_noise_labels = ["white_noise"] * white_noise_features.shape[0]

    print "Features computed, beginning training...."

    all_features = np.vstack((white_noise_features, voice_features))
    all_labels = np.concatenate((white_noise_labels, voice_labels))
    clf = train_knn(all_features, all_labels, n_neighbors=5)

    print "Training completed, testing..."

    white_noise_tests = files_to_mfcc_features('white_noise/test')
    voice_tests = files_to_mfcc_features('an4/wav/an4test_clstk')

    print "White noise test:", test_knn(clf, white_noise_tests)
    print "Voice test:", test_knn(clf, voice_tests)