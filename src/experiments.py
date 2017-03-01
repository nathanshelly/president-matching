from mfcc_knn import files_to_mfcc_features, train_knn, test_knn
import numpy as np

def experiment1(n_neighbors=5):
    """
    Train a knn model on ~1000 white noise and ~1000 voice snippets.
    Test with ~20 held out white noise and voice snippets.
    """
    voice_features, _ = files_to_mfcc_features('data/an4/wav/an4_clstk')
    voice_labels = ["voice"] * voice_features.shape[0]

    white_noise_features, _ = files_to_mfcc_features('data/white_noise/train')
    white_noise_labels = ["white_noise"] * white_noise_features.shape[0]

    print "Features computed, beginning training...."

    all_features = np.vstack((white_noise_features, voice_features))
    all_labels = np.concatenate((white_noise_labels, voice_labels))
    clf = train_knn(all_features, all_labels, n_neighbors)

    print "Training completed, testing..."

    white_noise_tests, _ = files_to_mfcc_features('data/white_noise/test')
    voice_tests, _ = files_to_mfcc_features('data/an4/wav/an4test_clstk')

    print "White noise test:", test_knn(clf, white_noise_tests)
    print "Voice test:", test_knn(clf, voice_tests)

def experiment2(n_neighbors=3):
    """
    Train a knn with 12 voice samples from each of 6 people (3 male, 3 female), and 12 samples of white noise.
    Test with 1 voice sample from each of the 6, and 1 sample of white noise.
    """

    train_data, train_labels = files_to_mfcc_features('data/an4_pairwise/train_full')
    clf = train_knn(train_data, train_labels, n_neighbors)

    test_data, exp_labels = files_to_mfcc_features('data/an4_pairwise/test_full')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data), exp_labels)]

def experiment3(n_neighbors=3):
    """
    Train a knn with 12 voice samples from each of 2 people (1 male, 1 female), and 12 samples of white noise.
    Test with 1 voice sample from each of the people, and 1 sample of white noise.
    """

    train_data, train_labels = files_to_mfcc_features('data/an4_pairwise/train')
    clf = train_knn(train_data, train_labels, n_neighbors)

    test_data, exp_labels = files_to_mfcc_features('data/an4_pairwise/test')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data), exp_labels)]

def experiment4(n_neighbors=3):
    """
    Train a knn with 8 voice samples from each of Nathan and Sasha, and 8 samples of white noise.abs
    Test with one voice sample from each of us, and one sample of white noise.
    """

    train_data, train_labels = files_to_mfcc_features('data/natasha_pairwise/train')
    clf = train_knn(train_data, train_labels, n_neighbors)

    test_data, exp_labels = files_to_mfcc_features('data/natasha_pairwise/test')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data), exp_labels)]

    
