from sklearn.neighbors import KNeighborsClassifier
import numpy as np

def train_knn(data, labels, n_neighbors=5):
    """
    Train and return a KNN model
    """
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(data, labels)
    return clf

def test_knn(knn_classifier, data):
    """Runs trained knn on each signal in set of signals"""
    def mode(lst):
        counter = {k:0 for k in set(lst)}
        for e in lst:
            counter[e] += 1
        
        return max(counter.iteritems(), key=lambda (k, v): v)[0]

    all_preds = [knn_classifier.predict(matrix) for matrix in data]
    return map(mode, all_preds)
