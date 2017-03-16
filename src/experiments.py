from mfcc import files_to_mfcc_features, unfold_matrix_list_with_labels
from gmm import train_gmm_set, test_gmms
from knn import train_knn, test_knn
import numpy as np
import utilities

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
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    clf = train_knn(new_train_data, new_train_labels, n_neighbors)

    test_data, exp_labels = files_to_mfcc_features('data/an4_pairwise/test_full')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data, list(set(exp_labels))), exp_labels)]

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
    Train a knn with 7 voice samples from each of Nathan and Sasha
    Test with two voice samples from each of us.
    """

    train_data, train_labels = files_to_mfcc_features('data/natasha_pairwise/train')
    clf = train_knn(train_data, train_labels, n_neighbors)

    test_data, exp_labels = files_to_mfcc_features('data/natasha_pairwise/test')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data), exp_labels)]

def experiment5(n_neighbors=3):
    """
    Train a knn with 7 voice samples from each of Nathan, Sasha, and Pardo
    Test with two voice samples from each of us
    """
    train_data, train_labels = files_to_mfcc_features('data/natasha_and_pardo/train')
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)
    clf = train_knn(new_train_data, new_train_labels, n_neighbors)
    utilities.save(clf, 'nathan_sasha_pardo_knn_clf.p')

    test_data, exp_labels = files_to_mfcc_features('data/natasha_and_pardo/test')

    print [(test, exp, test == exp) for test, exp in zip(test_knn(clf, test_data, list(set(exp_labels))), exp_labels)]

def experiment6():
    """
    Train a gmm with 7 voice samples from each of Nathan, Sasha, and Pardo
    Test with two voice samples from each of us
    """
    train_data, train_labels = files_to_mfcc_features('data/natasha_and_pardo/train')
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    utilities.save(gmm_dict, 'nathan_sasha_pardo_gmm_dict.p')
    
    test_data, exp_labels = files_to_mfcc_features('data/natasha_and_pardo/test')
    
    print [(test, exp, test == exp) for test, exp in zip(test_gmms(gmm_dict, test_data), exp_labels)]

def experiment7():
    """ Train a gmm with 12 voice samples from each of 6 people (3 male, 3 female), and 12 samples of white noise. 
        Test with 1 voice sample from each of the 6, and 1 sample of white noise. """
    train_data, train_labels = files_to_mfcc_features('data/an4_pairwise/train_full')
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    
    test_data, exp_labels = files_to_mfcc_features('data/an4_pairwise/test_full')
    
    print [(test, exp, test == exp) for test, exp in zip(test_gmms(gmm_dict, test_data), exp_labels)]

def experiment8():
    """Train a gmm with ~12 voice samples from each of 19 people and 1 set of white noise.

    Test with 1-2 voice samples from each class."""
    train_data, train_labels = files_to_mfcc_features('data/lots_of_people/train')
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    
    test_data, exp_labels = files_to_mfcc_features('data/lots_of_people/test')
    
    results = [(test, exp, test == exp) for test, exp in zip(test_gmms(gmm_dict, test_data), exp_labels)]
    print results
    print

    for res in results:
        if res[2]:
            print "Matched %s to %s -- correct" % (res[1], res[0])
        else:
            print "Expected %s, got %s -- incorrect" % (res[1], res[0])

    n_correct = len([r for r in results if r[2]])
    n_total = len(results)
    n_incorrect = n_total - n_correct
    print "%d/%d correct (%0.2f)" % (n_correct, n_total, float(n_correct)/n_total)
    print "%d/%d incorrect (%0.2f)" % (n_incorrect, n_total, float(n_incorrect)/n_total)

def experiment9():
    """Train a gmm with a bunch of samples from ~20 CS professors and Sara's kid.

    Test with 1-2 voice samples from each class."""
    train_data, train_labels = files_to_mfcc_features('data/professors_split/train')
    unique_train_labels = set(train_labels)
    gmm_train_data = {label: [] for label in unique_train_labels}
    new_train_data, new_train_labels = unfold_matrix_list_with_labels(train_data, train_labels)

    for feature_vector, label in zip(new_train_data, new_train_labels):
        gmm_train_data[label].append(feature_vector)

    gmm_dict = train_gmm_set(gmm_train_data)
    utilities.save(gmm_dict, 'professor_gmms.p')

    
    test_data, exp_labels = files_to_mfcc_features('data/professors_split/test')
    
    preds, probs = test_gmms(gmm_dict, test_data)
    results = [(test, exp, test == exp) for test, exp in zip(preds, exp_labels)]
    # print results
    # print

    # for i in range(len(probs)):
    #     print exp_labels[i]
    #     for prob in probs[i]:
    #         print prob
    #     print
    #     print

    for res in results:
        if res[2]:
            print "Matched %s to %s -- correct" % (res[1], res[0])
        else:
            print "Expected %s, got %s -- incorrect" % (res[1], res[0])

    n_correct = len([r for r in results if r[2]])
    n_total = len(results)
    n_incorrect = n_total - n_correct
    print "%d/%d correct (%0.2f)" % (n_correct, n_total, float(n_correct)/n_total)
    print "%d/%d incorrect (%0.2f)" % (n_incorrect, n_total, float(n_incorrect)/n_total)
