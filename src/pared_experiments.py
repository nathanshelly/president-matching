from mfcc import mfcc
from features import files_to_features, unfold_matrix_list_with_labels, knn_train_features
from gmm import train_gmm_set, test_gmms
from knn import train_knn, test_knn
import numpy as np
import utilities

def experiment1():
    """Train a knn with a bunch of samples from ~20 CS professors and Sara's kid.

    Test with 1 voice samples from each class."""
    train_data, train_labels = utilities.load('pickles/professor_knn_features_train.p')

    clf = train_knn(train_data, train_labels, n_neighbors=5)
    
    test_data, exp_labels = files_to_features('data/professors_split/test')
    
    preds = test_knn(clf, test_data)
    results = [(test, exp, test == exp) for exp, test in zip(preds, exp_labels)]

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

def experiment2():
    """Train a gmm with a bunch of samples from ~20 CS professors and Sara's kid.

    Test with 1-2 voice samples from each class."""
    gmm_dict = utilities.load('pickles/professor_gmms_train.p')
    
    test_data, exp_labels = files_to_features('data/professors_split/test')
    
    preds, probs = test_gmms(gmm_dict, test_data)
    results = [(test, exp, test == exp) for test, exp in zip(preds, exp_labels)]

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

def experiment3():
    """Check a bunch of local recordings of myself in different rooms against the professors,
    and see if they're consistent.

    Parsing out if trouble is matching different recording scenarios vs jumbled on server."""

    gmm_dict = utilities.load('pickles/professor_gmms.p')

    test_data, locations = files_to_features('data/sasha_rooms')
    preds, probs = test_gmms(gmm_dict, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Sasha (top prediction and top six in prediction order):\n"
    for i in range(len(locations)):
        print "Top prediction:", probs[i][-1][0]
        print "Top six:", [name for name, _ in reversed(probs[i][-6:])]
        print

    test_data, locations = files_to_features('data/nathan_rooms')
    preds, probs = test_gmms(gmm_dict, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Nathan (top prediction and top six in prediction order):\n"
    for i in range(len(locations)):
        print "Top prediction:", probs[i][-1][0]
        print "Top six:", [name for name, _ in reversed(probs[i][-6:])]
        print

def experiment4():
    """Check a bunch of downloaded website recordings of myself in the same room
    against the professors, and see if they're consistent.

    Same goal as experiment 10."""

    gmm_dict = utilities.load('pickles/professor_gmms.p')

    test_data, labels = files_to_features('data/sasha_website')

    preds, probs = test_gmms(gmm_dict, test_data)

    for i in range(len(probs)):
        print labels[i], probs[i]
        print

def experiment6():
    """Check a bunch of local recordings of myself in different rooms against the professors,
    and see if they're consistent, using KNNs.

    Parsing out if trouble is matching different recording scenarios vs jumbled on server."""
    train_data, train_labels = utilities.load('pickles/professor_knn_features.p')

    clf = train_knn(train_data, train_labels, n_neighbors=5)

    test_data, locations = files_to_features('data/sasha_rooms')

    preds = test_knn(clf, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Sasha (top predictions):\n"
    for i in range(len(locations)):
        print "Top prediction:", preds[i]
        print

    test_data, locations = files_to_features('data/nathan_rooms')

    preds = test_knn(clf, test_data)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Nathan (top predictions):\n"
    for i in range(len(locations)):
        print "Top prediction:", preds[i]
        print

